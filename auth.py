"""
auth.py
=======
Simple, static API-key authentication for the "write" endpoints
(POST, PUT, DELETE) of the management APIs.

How it works:
    - The server reads ADMIN_API_KEY from the environment (.env file).
    - Every protected endpoint depends on `verify_api_key`.
    - The client must send the key in an "X-API-Key" HTTP header.
    - If the header is missing or the key doesn't match -> HTTP 401.

GET endpoints (reading data for the public website) are NOT protected,
since the frontend needs to display this content to every visitor.
"""

import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# Read the admin key from the environment. Falls back to a dev default
# (CHANGE THIS in your .env file before deploying!).
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "my-secret-admin-key")

# This tells FastAPI/Swagger to look for the key in a header called "X-API-Key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(provided_key: str = Security(api_key_header)) -> str:
    """
    FastAPI dependency. Add `dependencies=[Depends(verify_api_key)]`
    to any route that should require the admin API key.
    """
    if provided_key is None or provided_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. Send it in the 'X-API-Key' header.",
        )
    return provided_key