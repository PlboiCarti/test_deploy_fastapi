from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from blog import schemas

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "ab604dd8f9dfbe4027637fc1948ab98dda4362e318317b4e9e7d0a50ed2e6958"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(data:str, credentials_exception):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub") # Giải phần subject trong token đã mã hóa ra để so khớp
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except InvalidTokenError:
        # Token hết hạn
        raise credentials_exception  