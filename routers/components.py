from typing import Optional

from fastapi import APIRouter, HTTPException, status
from models.components import (
    Component,
    ComponentCategory,
    GetComponentsResponse,
    CreateComponentResponse,
    DeleteComponentResponse,
    UpdateComponentRequest,
    PatchComponentRequest,
    UpdateComponentResponse,
)

router = APIRouter(tags=["components"])

componentes: list[Component] = [
    Component(id=1, name="Ryzen 5 5600X", brand="AMD",
              category=ComponentCategory.procesador, price=150.0),
    Component(id=2, name="Core i5-12400F", brand="Intel",
              category=ComponentCategory.procesador, price=130.0),
    Component(id=3, name="GeForce RTX 4060", brand="NVIDIA",
              category=ComponentCategory.placa_de_video, price=300.0),
    Component(id=4, name="Fury Beast 16GB DDR4", brand="Kingston",
              category=ComponentCategory.memoria_ram, price=45.0),
]


def buscar_componente(id: int) -> Component:
    """Devuelve el componente con ese id o lanza 404 si no existe."""
    for component in componentes:
        if component.id == id:
            return component

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Componente no encontrado"
    )


# Listado de componentes con filtros opcionales (se pueden combinar):
#   /component?category=procesador -> solo procesadores
#   /component?brand=amd           -> marca exacta (sin importar mayusculas)
#   /component?name=ryzen          -> nombre que contenga "ryzen"
#   /component?min_price=100&max_price=200 -> rango de precio
@router.get("/component")
def get_components(
    category: Optional[ComponentCategory] = None,
    brand: Optional[str] = None,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> GetComponentsResponse:
    filtrados = componentes
    if category is not None:
        filtrados = [c for c in filtrados if c.category == category]
    if brand is not None:
        filtrados = [c for c in filtrados
                     if c.brand.lower() == brand.lower()]
    if name is not None:
        filtrados = [c for c in filtrados
                     if name.lower() in c.name.lower()]
    if min_price is not None:
        filtrados = [c for c in filtrados if c.price >= min_price]
    if max_price is not None:
        filtrados = [c for c in filtrados if c.price <= max_price]

    return GetComponentsResponse(components=filtrados)


@router.get("/component/{id}")
def get_component(id: int) -> Component:
    return buscar_componente(id)


@router.post("/component")
def create_component(component: Component) -> CreateComponentResponse:
    if any(c.id == component.id for c in componentes):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un componente con ese id"
        )

    componentes.append(component)
    return CreateComponentResponse(message="componente creado")


# Modificacion completa: se reemplazan todos los datos del componente.
@router.put("/component/{id}")
def update_component(
    id: int, datos: UpdateComponentRequest
) -> UpdateComponentResponse:
    component = buscar_componente(id)
    component.name = datos.name
    component.brand = datos.brand
    component.category = datos.category
    component.price = datos.price
    return UpdateComponentResponse(
        message="componente modificado", component=component
    )


# Modificacion parcial: solo se cambian los campos enviados en el body.
@router.patch("/component/{id}")
def patch_component(
    id: int, datos: PatchComponentRequest
) -> UpdateComponentResponse:
    component = buscar_componente(id)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    for campo, valor in cambios.items():
        setattr(component, campo, valor)
    return UpdateComponentResponse(
        message="componente modificado", component=component
    )


@router.delete("/component/{id}")
def delete_component(id: int) -> DeleteComponentResponse:
    component = buscar_componente(id)
    componentes.remove(component)
    return DeleteComponentResponse(message="componente borrado")
