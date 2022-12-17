import datetime

from fastapi import Depends, HTTPException, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from starlette import status


class AuthHandler:
    # security = HTTPBearer()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    secret = "299a7c52d74dbc4b865e6cddf4150f8796b5c1cada75f4bb0cc087a99fec943c"
    # to get a string like this run:
    # openssl rand -hex 32

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, username: str):
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
            "iat": datetime.datetime.utcnow(),
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired signature")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, token: str = Security(oauth2_scheme)):
        return self.decode_token(token)

    # async def get_current_user(
    #     self,
    #     token: str = Security(oauth2_scheme),
    #     user_dao: UserDAO = Depends(),
    # ):
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #     )
    #     username = self.decode_token(token)
    #     if username is None:
    #         raise credentials_exception
    #     user = await user_dao.get_user_from_email(username)
    #     if user is None:
    #         raise credentials_exception
    #     return user
