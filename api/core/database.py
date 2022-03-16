
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, BaseDBAsyncClient
from core.settings import TORTOISE_ORM_CONFIG
from core.exceptions import (
    TokenExpirateError, TokenInvalidError, UnAuthorizedError,
    BadCredentialsError
)
from core.security import JWTBearer, verify_password, decode_token, oauth2_scheme
from jose import ExpiredSignatureError, JWTError
from models import User
from fastapi import Depends
from typing import Union


async def get_database(connection: str = 'default') -> BaseDBAsyncClient:
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    return Tortoise.get_connection(connection_name=connection)


def init_database(app):
    register_tortoise(app,
                      config=TORTOISE_ORM_CONFIG,
                      add_exception_handlers=True,
                      generate_schemas=True
                      )
    print('database connected')


async def is_authenticated(username: str, password: str) -> Union[bool, User]:
    user = await User.get_or_none(email=username)
    if not user:
        return False
    if not verify_password(password):
        return False
    return user


async def authenticate(username: str, password: str) -> User:
    user = await User.get_or_none(username=username)
    if not user:
        raise BadCredentialsError('Email or password incorrect.')
    if not verify_password(password, user.password):
        raise BadCredentialsError('Email or password incorrect.')
    return user


async def get_current_user(token: str = Depends(JWTBearer())):
    try:
        decoded_token = decode_token(token)
        user = await User.get_or_none(id=decoded_token.get('id'))
        if not user:
            raise UnAuthorizedError("Invalid authentication credentials")
        return user
    except ExpiredSignatureError:
        raise TokenExpirateError("Token expired. Get new one")
    except JWTError:
        raise TokenInvalidError("Invalid Token")


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_actif:
        raise UnAuthorizedError("Inactive user")
    return current_user
