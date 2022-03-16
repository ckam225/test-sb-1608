from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
import schemas
from services import AuthService, MediaService
from core.database import get_current_user
from core.medias import get_media
import os

router = APIRouter()


@router.post(path='/auth/register',   response_model=schemas.User, tags=['Auth'])
async def register(credentials: schemas.UserIn, repo: AuthService = Depends()):
    ''' Registration '''
    return await repo.register(credentials)


@router.post(path='/auth/login',  response_model=schemas.UserTokenSchema, tags=['Auth'])
async def login(credentials: schemas.LoginSchema, repo: AuthService = Depends()):
    ''' Authentication '''
    return await repo.login(credentials)


@router.get(path='/auth/me', summary="Get current user", response_model=schemas.User, tags=['Auth'])
async def get_auth_user(user: schemas.User = Depends(get_current_user)):
    ''' Get current user '''
    return user


@router.get("/medias", tags=['Medias'], response_model=list[schemas.Media])
async def get_images(limit: int = 100, skip: int = 0,  repo: MediaService = Depends(),
                     user: schemas.User = Depends(get_current_user)):
    return await repo.get_medias(skip=skip, limit=limit)


@router.get("/medias/stats", tags=['Medias'], response_model=schemas.MediaStats)
async def get_images_stats(repo: MediaService = Depends(), user: schemas.User = Depends(get_current_user)):
    return await repo.get_media_stats()


@router.post("/medias", tags=['Medias'])
async def upload_images(files: list[UploadFile] = File(...), category: str = Form(...),  repo: MediaService = Depends()):
    for file in files:
        if not file.content_type in ['image/jpeg', 'image/jpg', 'image/gif', 'image/png']:
            raise HTTPException(400, detail='Invalid image type')
    return await repo.create(files, category)


@router.get('/media/images/{path}', tags=['Medias'], summary="Get uploaded file")
async def get_image(*, path: str):
    name, ext = os.path.splitext(path)
    if not ext.lower() in ['.jpeg', '.gif', '.jpg', '.png']:
        raise HTTPException(400, detail='Invalid image type')
    return await get_media(path)
