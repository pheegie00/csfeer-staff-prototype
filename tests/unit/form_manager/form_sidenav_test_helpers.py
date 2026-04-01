import re
from html import unescape


def get_sidenav_markup(content: str) -> str:
    match = re.search(r'(<nav aria-label="Form sections">.*?</nav>)', content, re.DOTALL)
    assert match is not None
    return match.group(1)


def get_sidenav_link_markup(content: str, title: str) -> str:
    sidenav = get_sidenav_markup(content)
    match = re.search(rf"(<a\b[^>]*>\s*{re.escape(title)}\s*</a>)", sidenav)
    assert match is not None
    return match.group(1)


def get_sidenav_href(content: str, title: str) -> str:
    link_markup = get_sidenav_link_markup(content, title)
    match = re.search(r'href="([^"]+)"', link_markup)
    assert match is not None
    return unescape(match.group(1))
