"""Core views for health checks and utilities."""

from io import StringIO

from django.core.management import call_command
from django.db import connection
from django.http import JsonResponse


def health_check(request):
    """
    Liveness check - container is running and responding.

    This endpoint should always return 200 if the Django application
    can process requests. Used by container orchestration for liveness probes.
    """
    return JsonResponse({"status": "ok", "service": "csfeer"})


def readiness_check(request):
    """
    Readiness check - application is ready to serve traffic.

    Verifies:
    - Database connectivity
    - All migrations have been applied

    Returns 503 if the application is not ready to handle requests.
    Used by load balancers to determine if traffic should be routed.
    """
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Check migrations are applied
        out = StringIO()
        call_command("showmigrations", "--plan", stdout=out)
        output = out.getvalue()

        # Look for any unapplied migrations (marked with [ ])
        if "[ ]" in output:
            unapplied_count = output.count("[ ]")
            return JsonResponse(
                {
                    "status": "not_ready",
                    "reason": "unapplied_migrations",
                    "details": f"{unapplied_count} migration(s) pending",
                },
                status=503,
            )

        # All checks passed
        return JsonResponse({"status": "ready", "database": "connected", "migrations": "applied"})

    except Exception as e:
        # Any exception means we're not ready
        return JsonResponse(
            {"status": "not_ready", "reason": "error", "details": str(e)}, status=503
        )
