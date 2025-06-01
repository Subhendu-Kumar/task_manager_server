import os
import jwt
from typing import Dict
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.db_util import get_db

load_dotenv()
security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", 3600))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_token_bool(
    credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)
) -> bool:
    try:
        token = credentials.credentials
        if not token:
            return False
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        userId = payload.get("user")["id"]
        if not userId:
            return False
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            return False
        return True
    except ExpiredSignatureError:
        return False
    except InvalidTokenError:
        return False
