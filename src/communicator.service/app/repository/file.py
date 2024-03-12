from __future__ import annotations

import asyncio
import uuid
from typing import TYPE_CHECKING, Annotated

from aiofiles import open as async_open

from app.interfaces import IFile
from app.schemas import FileCreate, FileReposnse
from domain import BaseRepository
from domain.models import File
from infrastructure import SAVE_PATH, URL_PATH
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from litestar import Request
    from litestar.datastructures import UploadFile
    from litestar.enums import RequestEncodingType
    from litestar.params import Body

    from domain.auth import EntityAuth


class FileRepository(IFile):
    _repository: BaseRepository = BaseRepository(File)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def create(
            cls, data: Annotated[list[UploadFile], Body(media_type=RequestEncodingType.MULTI_PART)],
            request: Request = None,
    ) -> list[FileReposnse]:
        SAVE_PATH.mkdir(exist_ok=True)

        auth = cls._auth(request)
        await auth.verify(auth)

        url_path = URL_PATH
        save_path = SAVE_PATH

        async def save_file(file: UploadFile) -> FileReposnse:
            filename = file.filename
            random_filename = f"{uuid.uuid4()}_{filename}"
            async with async_open(save_path / random_filename, "wb") as f:
                await cls._repository.create_entity(
                    FileCreate(name=filename, path=str(url_path / random_filename)).model_dump(exclude_none=True))
                contents = await file.read()
                await f.write(contents)
            file_path = save_path / random_filename
            file_size = file_path.stat().st_size
            return FileReposnse(name=filename, path=str(url_path / random_filename), size=file_size)

        tasks = [save_file(file) for file in data]
        return await asyncio.gather(*tasks)

