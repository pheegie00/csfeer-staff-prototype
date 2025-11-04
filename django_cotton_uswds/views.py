from django.shortcuts import render


def component_gallery(request):
    """Dev-only gallery view to preview packaged cotton components."""
    # Example context that may be useful to components that expect slots/attrs
    context = {
        "example_list": ["One", "Two", "Three"],
    }
    return render(request, "django_cotton_uswds/gallery.html", context)
