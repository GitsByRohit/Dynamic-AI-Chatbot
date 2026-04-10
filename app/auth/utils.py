from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.auth_queries import get_user_by_email

# -----------------------------------------
# SECURITY SETTINGS
# -----------------------------------------

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer scheme for Swagger token input
security = HTTPBearer()


# -----------------------------------------
# PASSWORD HASHING
# -----------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------------------
# CREATE JWT TOKEN
# -----------------------------------------

def create_access_token(data: dict, expires_delta: timedelta):

    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# -----------------------------------------
# GET CURRENT USER (JWT VALIDATION)
# -----------------------------------------

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email)

    if user is None:
        raise credentials_exception

    return user