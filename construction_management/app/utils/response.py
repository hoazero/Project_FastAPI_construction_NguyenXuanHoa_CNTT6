from datetime import datetime, timezone
from fastapi import Request, status


def success_response(
    request: Request,
    data=None,
    message="Success"
):
    return {
        "status_code": status.HTTP_200_OK,
        "message": message,
        "data": data,
        "errors": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": request.url.path
    }


def error_response(
    request: Request,
    status_code: int,
    message: str,
    errors=None
):
    return {
        "status_code": status_code,
        "message": message,
        "data": None,
        "errors": errors,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": request.url.path
    }