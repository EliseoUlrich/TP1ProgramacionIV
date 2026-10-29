from typing import Optional

from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
    UpdateUserRequest,
    PatchUserRequest,
    UpdateUserResponse,
)

router = APIRouter(tags=["users"])

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
]


def buscar_usuario(id: int) -> User:
    """Devuelve el usuario con ese id o lanza 404 si no existe."""
    for user in usuarios:
        if user.id == id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# Listado de usuarios con filtro opcional por estado:
#   /user                 -> todos
#   /user?is_active=true  -> solo activos
#   /user?is_active=false -> solo inactivos
@router.get("/user")
def get_users(is_active: Optional[bool] = None) -> GetUsersResponse:
    if is_active is None:
        r = GetUsersResponse(users=usuarios)
    else:
        filtrados = [u for u in usuarios if u.is_active == is_active]
        r = GetUsersResponse(users=filtrados)
    return r


@router.get("/user/{id}")
def get_user(id: int) -> User:
    return buscar_usuario(id)


@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="ususario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@router.post("/user")
def create_user(user: User) -> CreateUserResponse:
    if any(u.id == user.id for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese id"
        )

    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")


# Modificacion completa: se reemplazan todos los datos del usuario.
@router.put("/user/{id}")
def update_user(id: int, datos: UpdateUserRequest) -> UpdateUserResponse:
    user = buscar_usuario(id)
    user.name = datos.name
    user.is_active = datos.is_active
    return UpdateUserResponse(message="usuario modificado", user=user)


# Modificacion parcial: solo se cambian los campos enviados en el body.
@router.patch("/user/{id}")
def patch_user(id: int, datos: PatchUserRequest) -> UpdateUserResponse:
    user = buscar_usuario(id)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    for campo, valor in cambios.items():
        setattr(user, campo, valor)
    return UpdateUserResponse(message="usuario modificado", user=user)
