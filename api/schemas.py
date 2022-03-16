from itertools import count
from pydantic import BaseModel, validator, Field
from fastapi import File, UploadFile
from typing import Optional
from datetime import datetime


def datetime_str(dt: datetime) -> str:
    return dt.isoformat()


class PasswordSchema(BaseModel):
    password: str = Field(..., min_length=4,
                          description='Password must be at least 4 characters')
    password2: str

    @validator('password')
    def check_valid_password(cls, value):
        if not (any(a for a in value if str(a).isalpha())
                and any(a for a in value if str(a).isdigit())):
            raise ValueError(
                'Password must contain at least character and number')
        elif not any([s for s in '#$(&}?!{;@)*%' if s in value]):
            raise ValueError(
                'Password must contain at least special character')
        elif value.islower() or value.isupper():
            raise ValueError(
                'Password must contain at least lower and upper character')
        else:
            return value

    @validator('password2')
    def check_passwords_matching(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError('Passwords do not match')
        return value


class UserIn(BaseModel):
    name: str
    username: str
    password: Optional[str]
    telegram_id: Optional[str]


class User(BaseModel):
    id: Optional[int]
    name: str
    username: str
    on_bot: bool = False
    telegram_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: datetime_str
        }
        orm_mode = True


class UserTokenSchema(User):
    access_token: str
    token_type: Optional[str]
    token_expire_at: Optional[datetime]


class LoginSchema(BaseModel):
    password: str
    username: str


class Media(BaseModel):
    id: Optional[int]
    name: str
    category: Optional[str]
    url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: datetime_str
        }
        orm_mode = True


class MediaIn(BaseModel):
    category: Optional[str]
    files: list[UploadFile] = File(...)


class MediaCategoyCount(BaseModel):
    category: Optional[str]
    count: int


class MediaStats(BaseModel):
    media_count: int
    vote_count: int
    by_category: list[MediaCategoyCount]
