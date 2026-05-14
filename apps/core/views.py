import os

from django.db import connection
from django.http import JsonResponse


def health(request):
    """Liveness/readiness probe for load balancers and local smoke checks."""
    db_ok = True
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as exc:  # noqa: BLE001 — surface failure in payload
        db_ok = False
        db_error = str(exc)
    else:
        db_error = ""

    payload = {
        "status": "healthy" if db_ok else "degraded",
        "service": "beatiq-api",
        "version": os.environ.get("BEATIQ_API_VERSION", "1"),
        "database": "ok" if db_ok else "error",
    }
    if not db_ok:
        payload["database_error"] = db_error[:500]
    status = 200 if db_ok else 503
    return JsonResponse(payload, status=status)
