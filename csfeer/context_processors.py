from django.conf import settings


def app_version(request):
    return {
        "APP_VERSION": settings.APP_VERSION,
        "SHOW_APP_VERSION": settings.SHOW_APP_VERSION,
    }
