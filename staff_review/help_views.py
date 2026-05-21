"""Help section views (Phase 4 Step 9).

Three URLs:
  /staff/help/                  -- role-filtered index + chatbot widget
  /staff/help/<slug>/           -- single article
  /staff/help/chat/             -- POST endpoint for chatbot turns

All three are gated by the help_section feature flag. The chatbot is
additionally gated by help_chatbot so a presenter can show articles
without the chat widget if desired.
"""

from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from staff_review.feature_flags import FeatureRequiredMixin, is_enabled
from staff_review.help_chatbot import answer as chatbot_answer
from staff_review.help_content import (
    article_by_slug,
    articles_for,
    audiences_for_user,
)


# Session key for the chat transcript (one independent thread per session)
CHAT_SESSION_KEY = "help_chat_history"
CHAT_MAX_TURNS = 20  # cap so the session doesn't bloat indefinitely


class HelpIndexView(FeatureRequiredMixin, LoginRequiredMixin, TemplateView):
    """Quick start + KB articles grouped by category + chatbot widget."""

    feature_key = "help_section"
    template_name = "staff_review/help_index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.request.user
        audiences = audiences_for_user(u)
        articles = articles_for(audiences)

        # Group by category preserving the order they were registered in
        grouped: OrderedDict[str, list] = OrderedDict()
        for a in articles:
            grouped.setdefault(a.category, []).append(a)

        ctx.update({
            "audiences": sorted(audiences),
            "articles_by_category": grouped,
            "total_articles": len(articles),
            "chatbot_enabled": is_enabled("help_chatbot"),
            "chat_history": self.request.session.get(CHAT_SESSION_KEY, []),
        })
        return ctx


class HelpArticleView(FeatureRequiredMixin, LoginRequiredMixin, TemplateView):
    """Single article. 404 if the slug is unknown OR not in the user's audience."""

    feature_key = "help_section"
    template_name = "staff_review/help_article.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = kwargs.get("slug")
        article = article_by_slug(slug)
        if article is None:
            raise Http404(f"No help article with slug {slug!r}")

        audiences = audiences_for_user(self.request.user)
        if not (set(article.audiences) & audiences):
            # Don't reveal that the article exists; 404 instead of 403
            # to avoid leaking which articles are reserved for other roles.
            raise Http404(f"No help article with slug {slug!r}")

        # Suggest related articles in the same category, excluding self
        related = [
            a for a in articles_for(audiences)
            if a.category == article.category and a.slug != article.slug
        ][:4]

        ctx.update({
            "article": article,
            "related": related,
        })
        return ctx


class HelpChatView(FeatureRequiredMixin, LoginRequiredMixin, View):
    """POST a question, append the turn + assistant response to the session transcript."""

    feature_key = "help_section"
    http_method_names = ["post"]

    def post(self, request):
        # Sub-gate: chatbot can be off even when Help is on
        if not is_enabled("help_chatbot"):
            return redirect(reverse("staff_review:help_index"))

        query = (request.POST.get("query") or "").strip()
        if request.POST.get("reset"):
            request.session[CHAT_SESSION_KEY] = []
            return redirect(reverse("staff_review:help_index") + "#chat")

        if not query:
            return redirect(reverse("staff_review:help_index") + "#chat")

        history = list(request.session.get(CHAT_SESSION_KEY, []))
        history.append({"role": "user", "text": query, "articles": []})

        resp = chatbot_answer(request.user, query)
        history.append({
            "role": "assistant",
            "text": resp.framing,
            "articles": [
                {"slug": a.slug, "title": a.title, "summary": a.summary}
                for a in resp.articles
            ],
            "fallback": resp.fallback,
        })

        # Cap session size
        if len(history) > CHAT_MAX_TURNS * 2:
            history = history[-CHAT_MAX_TURNS * 2:]
        request.session[CHAT_SESSION_KEY] = history

        return redirect(reverse("staff_review:help_index") + "#chat")
