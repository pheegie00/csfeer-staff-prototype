"""Alias module to make django-cotton templatetags available via a simple builtin.

Add the path `django_cotton_uswds.templatetags.cotton_aliases` to
TEMPLATES[...]['OPTIONS']['builtins'] if you want the cotton tags to be
available everywhere without `{% load cotton %}`.

This module simply imports the real `django_cotton.templatetags.cotton`
module so that its `register` definition is imported by Django's template
library loader.
"""

from django_cotton.templatetags import cotton  # noqa: F401

# expose the `register` object so Django's template loader accepts this
# module as a template library when used in TEMPLATES[...]['OPTIONS']['builtins']
try:
    register = cotton.register
except Exception:
    # fallback: if the cotton module doesn't expose register for any reason,
    # leave `register` undefined so Django will surface an informative error.
    pass
