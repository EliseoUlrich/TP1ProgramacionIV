from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


# Categorias posibles de un componente de PC.
class ComponentCategory(str, Enum):
    procesador = "procesador"
    placa_de_video = "placa_de_video"
    memoria_ram = "memoria_ram"
    motherboard = "motherboard"
    almacenamiento = "almacenamiento"
    fuente = "fuente"
    gabinete = "gabinete"
    refrigeracion = "refrigeracion"


# Entidad propia: Componente de PC, con 5 campos.
class Component(BaseModel):
    id: int
    name: str                    # modelo, ej: "Ryzen 5 5600X"
    brand: str                   # marca, ej: "AMD"
    category: ComponentCategory  # tipo de componente
    price: float = Field(gt=0)   # precio en dolares


class GetComponentsResponse(BaseModel):
    components: List[Component]


class CreateComponentResponse(BaseModel):
    message: str


class DeleteComponentResponse(BaseModel):
    message: str


# Body para modificar un componente completo (PUT).
# El id no se incluye porque viene en la URL.
class UpdateComponentRequest(BaseModel):
    name: str
    brand: str
    category: ComponentCategory
    price: float = Field(gt=0)


# Body para modificar parcialmente un componente (PATCH).
# Todos los campos son opcionales: solo se cambian los que se envian.
class PatchComponentRequest(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[ComponentCategory] = None
    price: Optional[float] = Field(default=None, gt=0)


class UpdateComponentResponse(BaseModel):
    message: str
    component: Component
