from typing import Annotated

from litestar import Controller, Request, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body

from app.repository.file import FileRepository
from app.schemas import FileReposnse


class File(Controller):
    _file_repository = FileRepository

    @post(path="/")
    async def file_upload(
            self,
            data: Annotated[list[UploadFile], Body(media_type=RequestEncodingType.MULTI_PART)], request: Request,
    ) -> list[FileReposnse]:
        return await self._file_repository.create(data, request)
