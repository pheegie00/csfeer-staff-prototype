"""KB-grounded help chatbot (Phase 4 Step 9).

This is NOT an LLM. It is a keyword-scoring search assistant that
returns existing KB articles wrapped in canned framing. We chose
this on purpose for the prototype: predictable, audit-friendly,
no API surface to a third party, and easy to expand by writing
more articles.

Algorithm:
  1. Tokenize the user's query (lowercase, strip punctuation, drop
     stopwords).
  2. Score every article visible to the user's audience set:
       +3 per query token found in the title
       +2 per query token found in keywords
       +1 per query token found in the summary or body
       +1 bonus for the article's category if it matches a token
  3. Return the top N (default 2) articles whose score >= threshold.
  4. If no article meets threshold, return a fallback message with
     links to the user's category list so they can browse.

The framing message is canned: "Here's what I found about ..." plus a
copy-pasted snippet of the article summary. We never invent answers.
"""

import re
import string
from dataclasses import dataclass

from staff_review.help_content import (
    Article,
    articles_for,
    audiences_for_user,
)


# Common English stopwords that add noise to the scorer
_STOPWORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "then", "else", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "as", "i", "you", "we", "they",
    "it", "this", "that", "these", "those", "do", "does", "did", "doing",
    "have", "has", "had", "will", "would", "could", "should", "may",
    "might", "must", "can", "what", "when", "where", "why", "how", "who",
    "which", "my", "your", "our", "their", "me", "us", "him", "her",
    "them", "about", "into", "through", "during", "before", "after",
    "above", "below", "up", "down", "out", "off", "over", "under",
    "again", "further", "once", "here", "there", "all", "any", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "now",
})


# Lightweight synonym map so common phrasings hit the right articles
# even when the article uses the canonical term.
_SYNONYMS = {
    "send back": ["return"],
    "revise": ["return"],
    "revision": ["return"],
    "deadline": ["window", "closes"],
    "due": ["window", "closes", "deadline"],
    "deny": ["close"],
    "denied": ["close", "closed"],
    "approve": ["accept", "determination"],
    "approved": ["accept", "accepted"],
    "approval": ["accept", "determination"],
    "decision": ["determination"],
    "publish": ["publish", "new version"],
    "release": ["publish"],
    "log": ["audit", "log"],
    "switch": ["view as", "persona"],
    "impersonate": ["view as", "persona"],
    "swap": ["view as", "persona"],
    "toggle": ["feature flag", "feature"],
    "disable": ["feature flag", "off"],
    "enable": ["feature flag", "on"],
    "scoping": ["scope", "org type"],
    "eligibility": ["scope", "eligible"],
}


@dataclass(frozen=True)
class ChatbotResponse:
    """Structured answer the view template iterates over."""

    framing: str            # "Here's what I found..." canned intro
    articles: list[Article]  # ordered best-first, may be empty
    fallback: bool          # True if no article met threshold
    query: str              # echoed back for the chat transcript


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, drop stopwords + very short tokens."""
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", " ", text)
    raw = text.split()
    return [t for t in raw if len(t) > 2 and t not in _STOPWORDS]


def _expand_with_synonyms(tokens: list[str], raw_query: str) -> set[str]:
    """Augment the token set with mapped synonyms (acts on both tokens + raw phrases)."""
    expanded = set(tokens)
    lowered = raw_query.lower()
    for phrase, mapped in _SYNONYMS.items():
        if phrase in lowered:
            for syn in mapped:
                for t in _tokenize(syn):
                    expanded.add(t)
    return expanded


def _score(article: Article, tokens: set[str]) -> int:
    """Sum the weighted hits per article."""
    if not tokens:
        return 0
    title_tokens = set(_tokenize(article.title))
    kw_tokens = set()
    for kw in article.keywords:
        kw_tokens.update(_tokenize(kw))
    summary_tokens = set(_tokenize(article.summary))
    body_tokens = set(_tokenize(article.body))
    category_tokens = set(_tokenize(article.category))

    score = 0
    for t in tokens:
        if t in title_tokens:
            score += 3
        if t in kw_tokens:
            score += 2
        if t in summary_tokens:
            score += 1
        if t in body_tokens:
            score += 1
        if t in category_tokens:
            score += 1
    return score


def answer(user, query: str, top_n: int = 2, score_threshold: int = 2) -> ChatbotResponse:
    """Build a response for `user` to a question `query`.

    Returns a ChatbotResponse with up to `top_n` articles. If no
    article scores at least `score_threshold`, returns a fallback
    message with `articles=[]` and `fallback=True`.
    """
    clean = (query or "").strip()
    if not clean:
        return ChatbotResponse(
            framing="Type a question above and I will look it up in the knowledge base.",
            articles=[],
            fallback=True,
            query="",
        )

    audiences = audiences_for_user(user)
    visible = articles_for(audiences)
    tokens = _expand_with_synonyms(_tokenize(clean), clean)

    scored = [(a, _score(a, tokens)) for a in visible]
    scored = [(a, s) for a, s in scored if s >= score_threshold]
    scored.sort(key=lambda x: (-x[1], x[0].title))
    top = [a for a, _ in scored[:top_n]]

    if not top:
        return ChatbotResponse(
            framing=(
                "I could not find a knowledge base article that matches "
                "that question for your role. Try rephrasing, or browse "
                "the categories on the Help page."
            ),
            articles=[],
            fallback=True,
            query=clean,
        )

    framing = (
        "Here is what I found in the knowledge base. "
        "Click any article for the full answer."
        if len(top) > 1
        else "Here is what I found. Open the article for the full answer."
    )
    return ChatbotResponse(
        framing=framing,
        articles=top,
        fallback=False,
        query=clean,
    )
