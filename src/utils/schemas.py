from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    exp: Optional[int] = None
