import hashlib
import hmac
import re
import time

from fastapi import HTTPException, Request

from app.core.config import get_settings


async def verify_retell_request(request: Request) -> bytes:
    settings = get_settings()

    signature = request.headers.get("X-Retell-Signature")

    if not signature:
        raise HTTPException(
            status_code=401,
            detail="Missing Retell signature.",
        )

    raw_body = await request.body()

    match = re.fullmatch(r"v=(\d+),d=(.*)", signature)

    if not match:
        raise HTTPException(
            status_code=401,
            detail="Invalid Retell signature format.",
        )

    timestamp = match.group(1)
    received_digest = match.group(2)

    try:
        timestamp_ms = int(timestamp)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Retell signature timestamp.",
        )

    current_time_ms = int(time.time() * 1000)

    if abs(current_time_ms - timestamp_ms) > 5 * 60 * 1000:
        raise HTTPException(
            status_code=401,
            detail="Expired Retell signature.",
        )

    if not settings.retell_api_key:
        raise HTTPException(
            status_code=500,
            detail="Retell API key is not configured.",
        )

    message = raw_body + timestamp.encode("utf-8")

    expected_digest = hmac.new(
        settings.retell_api_key.encode("utf-8"),
        message,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_digest, received_digest):
        raise HTTPException(
            status_code=401,
            detail="Invalid Retell signature.",
        )

    return raw_body