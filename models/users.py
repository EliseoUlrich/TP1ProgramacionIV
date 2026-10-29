from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # default value, field becomes optional


class GetUsersResponse(BaseModel):
    users: List[User]


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str


# Body para modificar un usuario completo (PUT).
# El id no se incluye porque viene en la URL.
class UpdateUserRequest(BaseModel):
    name: str
    is_active: bool = True


# Body para modificar parcialmente un usuario (PATCH).
# Todos los campos son opcionales: solo se cambian los que se envian.
class PatchUserRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UpdateUserResponse(BaseModel):
    message: str
    user: User
