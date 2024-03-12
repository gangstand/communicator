from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IAuth
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
from domain import BaseRepository
from domain.models import User
from domain.typing import Response
from infrastructure import ID_MANAGER
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from litestar import Request

    from app.schemas.auth import RefreshResponse
    from domain.auth import EntityAuth


class AuthRepository(IAuth):
    _repository: BaseRepository = BaseRepository(User)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def get_one(cls, request: Request = None) -> AuthUserRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        entity_id = auth.get_jwt_subject()
        user = await cls._repository.query_entity(id=entity_id)
        return AuthUserRead.from_orm(user)

    @classmethod
    async def update(cls, data: AuthUserUpdate, request: Request = None) -> AuthUserRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        entity_id = auth.get_jwt_subject()
        user = await cls._repository.update_entity(entity_id, data.model_dump(exclude_none=True))
        return AuthUserRead.from_orm(user)

    @classmethod
    async def create(cls, data: AuthUserCreate) -> AuthUserRead:
        auth = cls._auth()
        if len(data.password) > 1:
            data.password = await auth.hash_password(data.password)
        user = await cls._repository.create_entity(data.model_dump(exclude_none=True))
        return AuthUserRead.from_orm(user)

    @classmethod
    async def update_password(cls, data: AuthUserPasswordUpdate) -> Response:
        auth = cls._auth()
        entity_id = await auth.verify_token_password(data.token)
        data.password = await auth.hash_password(data.password)
        await cls._repository.update_entity(entity_id, data.model_dump(exclude_unset=True))
        return Response(message="Успешно")

    @classmethod
    async def login_email(cls, data: AuthUserLogin) -> LoginResponse:
        auth = cls._auth()
        user = await auth.verify_user(cls._repository, email=data.email)
        user = await auth.check_password(user, data)
        roles = [str(role.name) for role in user.roles]
        access_token = auth.create_access_token(subject=str(user.id), user_claims={"roles": roles})
        refresh_token = auth.create_refresh_token(subject=str(user.id), user_claims={"roles": roles})
        return LoginResponse(access=access_token, refresh=refresh_token)

    @classmethod
    async def login_phone(cls, data: AuthUserPhoneLogin) -> LoginResponse:
        auth = cls._auth()
        user = await auth.verify_user(cls._repository, email=data.phone)
        user = await auth.check_password(user, data)
        roles = [str(role.name) for role in user.roles]
        access_token = auth.create_access_token(subject=str(user.id), user_claims={"roles": roles})
        refresh_token = auth.create_refresh_token(subject=str(user.id), user_claims={"roles": roles})
        return LoginResponse(access=access_token, refresh=refresh_token)

    @classmethod
    async def refresh(cls, data: RefreshResponse) -> LoginResponse:
        token = data.refresh
        auth = cls._auth()
        auth.jwt_refresh_token_required(auth_from="refresh", token=token)
        entity_id = auth.get_raw_jwt(token)["sub"]
        user = await auth.verify_user(cls._repository, id=entity_id)
        roles = [str(role.name) for role in user.roles]
        access_token = auth.create_access_token(subject=str(user.id), user_claims={"roles": roles})
        refresh_token = auth.create_refresh_token(subject=str(user.id), user_claims={"roles": roles})
        return LoginResponse(access=access_token, refresh=refresh_token)

    @classmethod
    async def recovery(cls, data: Recovery) -> Response:
        auth = cls._auth()
        user = await auth.verify_user(cls._repository, email=data.email)
        await auth.create_token_password(user.id)
        return Response(message="Отправлено электронное письмо для восстановления пароля")

    @classmethod
    async def manager_token(cls, data: RefreshResponse) -> LoginResponse:
        token = data.refresh
        auth = cls._auth()
        auth.jwt_refresh_token_required(auth_from="refresh", token=token)
        access_token = auth.create_access_token(subject=ID_MANAGER)
        refresh_token = auth.create_refresh_token(subject=ID_MANAGER)
        return LoginResponse(access=access_token, refresh=refresh_token)
