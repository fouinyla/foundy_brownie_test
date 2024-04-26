from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from core.settings import appSettings


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if x_api_key != appSettings.AUTHENTICATION_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication Key")
    return x_api_key
