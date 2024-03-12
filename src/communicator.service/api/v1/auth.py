from litestar import Controller, Request, get, patch, post

from app.repository import AuthRepository
from app.schemas import (
    AuthUserCreate,
    AuthUserLogin,
    AuthUserPasswordUpdate,
    AuthUserPhoneLogin,
    AuthUserRead,
    AuthUserUpdate,
    LoginResponse,
    Recovery,
)
from app.schemas.auth import RefreshResponse
from domain.typing import Response


class Auth(Controller):
    _auth_repository = AuthRepository

    @get("/me")
    async def get_me(self, request: Request) -> AuthUserRead:
        return await self._auth_repository.get_one(request)

    @patch("/me")
    async def patch_me(self, data: AuthUserUpdate, request: Request) -> AuthUserRead:
        return await self._auth_repository.update(data, request)

    @post("/login/email")
    async def login_email(self, data: AuthUserLogin) -> LoginResponse:
        return await self._auth_repository.login_email(data)

    @post("/login/phone")
    async def login_phone(self, data: AuthUserPhoneLogin) -> LoginResponse:
        return await self._auth_repository.login_phone(data)

    @post("/signup")
    async def signup(self, data: AuthUserCreate) -> AuthUserRead:
        return await self._auth_repository.create(data)

    @post("/refresh")
    async def refresh(self, data: RefreshResponse) -> LoginResponse:
        return await self._auth_repository.refresh(data)

    @post("/recovery-password")
    async def recovery(self, data: Recovery) -> Response:
        return await self._auth_repository.recovery(data)

    @post("/reset-password")
    async def reset_password(self, data: AuthUserPasswordUpdate) -> Response:
        return await self._auth_repository.update_password(data)

    @post("/manager/token")
    async def manager_token(self, data: RefreshResponse) -> LoginResponse:
        return await self._auth_repository.manager_token(data)
