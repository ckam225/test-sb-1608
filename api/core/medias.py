from fastapi import Path, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
import shutil
import os
import uuid
from core.exceptions import FileDoesntExistError


base_dir = os.path.join(os.getcwd(), 'media')

if not os.path.exists(base_dir):
    os.mkdir(base_dir)


def upload_file(media: UploadFile = File(...), keep_origin_name: bool = True) -> str:
    filename = f"{uuid.uuid4()}{os.path.splitext(media.filename)[1]}" if not keep_origin_name else media.filename
    with open(f'{base_dir}/{filename}', 'wb+') as buffer:
        shutil.copyfileobj(media.file, buffer)
    return filename


def upload_multiple_files(files: List[UploadFile] = File(...), keep_origin_name: bool = True) -> list[str]:
    paths = []
    for f in files:
        f = upload_file(f, keep_origin_name=keep_origin_name)
        paths.append(f)
    return paths


async def get_media(filename: str):
    path = f'{base_dir}/{filename}'
    if os.path.exists(path):
        return FileResponse(path)
    raise FileDoesntExistError('File does not exist!')
