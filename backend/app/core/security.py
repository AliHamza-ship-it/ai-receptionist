import hmac
import hashlib

from fastapi import Header, HTTPException


def verify_retell_signature(
    body: bytes,
    signature: str | None = Header(None, alias="X-Retell-Signature"),
):
    if not signature:
        raise HTTPException(
            status_code=401,
            detail="Missing Retell signature.",
        )

    # Full Retell signature verification will be connected
    # when the Retell webhook/custom-function secret is configured.
    return True