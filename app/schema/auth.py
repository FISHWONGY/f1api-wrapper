from pydantic import BaseModel

from typing import Optional
from fastapi import Form


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    client_id: str | None = None


class TokenRequestForm:
    def __init__(
        self,
        # grant_type: str = Form(None, regex="client_credentials"),
        grant_type: Optional[str] = Form(..., regex="^(password|client_credentials)$"),
        client_id: Optional[str] = Form(...),
        client_secret: Optional[str] = Form(...),
    ):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
