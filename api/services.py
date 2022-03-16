from models import User, Media, Vote
import schemas
from fastapi import UploadFile
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.transactions import in_transaction
from tortoise.exceptions import OperationalError
from tortoise.functions import Count, Sum
from core.database import authenticate
from core.security import hash_password, create_access_token
from core.exceptions import (
    BadCredentialsError,
    ModelNotfoundError,
    UniqueFieldError
)
from core.medias import upload_multiple_files


class AuthService:

    serializer = pydantic_model_creator(User)

    async def register(self, schema: schemas.UserIn) -> User:
        ''' Registration user '''
        user_obj = User(**schema.dict(exclude={'password2'}))
        # if(User.filter(username=user_obj.username).count() > 0):
        #     raise UniqueFieldError('username already exists')
        # if(User.filter(telegram_id=user_obj.telegram_id).count() > 0):
        #     raise UniqueFieldError('telegram_id  already exists')
        user_obj.password = hash_password(user_obj.password)
        await user_obj.save()
        return await self.serializer.from_tortoise_orm(user_obj)

    async def login(self, schema: schemas.LoginSchema):
        ''' Authentication user '''
        user = await authenticate(
            username=schema.username,
            password=schema.password,
        )
        if not user:
            raise BadCredentialsError('Username or password incorrect.')
        token: dict = create_access_token({
            'id': user.id,
            'username': user.username
        })
        obj = self.serializer.from_orm(user).dict()
        obj['access_token'] = token.get('access_token')
        obj['token_type'] = token.get('token_type')
        obj['token_expire_at'] = token.get('token_expire_at')
        return obj

    async def is_on_telegram(self, telegram_id: str):
        await User.filter(on_bot=True, telegram_id=telegram_id).exists()

    async def login_to_telegrambot(self, telegram_id: str):
        obj = await User.get(telegram_id=telegram_id)
        if obj:
            obj.on_bot = True
            await obj.save()
            return self.serializer.from_orm(obj)
        raise ModelNotfoundError(
            f'Model not found with telegram_id ({telegram_id})')

    async def logout_to_telegrambot(self, telegram_id: str):
        obj = await User.get(telegram_id=telegram_id)
        if obj:
            obj = await obj.update_from_dict({'on_bot': False})
            obj = await self.serializer.from_queryset_single(obj)
            return obj
        raise ModelNotfoundError(f'Model not found with id ({telegram_id})')


class MediaService:
    serializer = pydantic_model_creator(Media)

    async def get_medias(self, skip: int = 0, limit: int = 100) -> list[Media]:
        s = await Media.all().offset(skip).limit(limit)
        return s

    async def create(self, data: list[UploadFile], category: str) -> list[Media]:
        output_files = []
        try:
            async with in_transaction() as connection:
                files = upload_multiple_files(data)
                for file in files:
                    media = Media(category=category, name=file, url=file)
                    await media.save(using_db=connection)
                    m = await self.serializer.from_tortoise_orm(media)
                    output_files.append(m)
        except OperationalError:
            pass
        return output_files

    async def get_media_stats(self):
        stats = {}
        media_count = await Media.all().count()
        vote_count = await Vote.all().count()
        category_count = await Media.annotate(count=Count('category')).group_by('category').values('category', 'count')
        stats['media_count'] = media_count
        stats['vote_count'] = vote_count
        stats['by_category'] = category_count
        return stats
