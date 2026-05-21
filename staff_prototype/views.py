"""Views for the staff_prototype app.

The prototype itself is a React/Babel SPA loaded from static assets. We
just need a single Django view that serves the index HTML; everything
else (data, atoms, screens, workflow) loads as static JS/CSS.
"""

from django.views.generic import TemplateView


class PrototypeIndex(TemplateView):
    """Serve the React-based staff workflow prototype."""

    template_name = "staff_prototype/index.html"
