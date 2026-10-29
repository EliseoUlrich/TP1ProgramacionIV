# Clase FastAPI

Clase para aprender **FastAPI** y **Pydantic**.

**Trabajo Práctico:** ABM de Usuarios + ABM propio de **Componentes de PC**.

---

## Requisitos previos

- **Python 3.12 o superior** instalado.
  - Windows: descargarlo de <https://www.python.org/downloads/> y, durante la
    instalación, **tildar la opción "Add python.exe to PATH"**.
  - macOS: `brew install python` (o el instalador de python.org).
  - Linux (Debian/Ubuntu): `sudo apt install python3 python3-venv python3-pip`
- **Git** (opcional, solo para clonar el repositorio).

Verificar la versión instalada:

```bash
# Windows
python --version

# macOS / Linux
python3 --version
```

---

## Instalación y ejecución

### 1. Obtener el código

```bash
git clone https://github.com/EliseoUlrich/TP1ProgramacionIV.git
cd TP1ProgramacionIV
```

> También se puede descargar el ZIP desde GitHub (**Code → Download ZIP**),
> descomprimirlo y abrir una terminal dentro de la carpeta descomprimida.

**Todos los comandos siguientes se ejecutan desde la carpeta `TP1ProgramacionIV`**
(donde está el archivo `main.py`).

### 2. Crear el entorno virtual (venv)

<table>
<tr><th>Windows (PowerShell)</th><th>macOS / Linux</th></tr>
<tr><td>

```powershell
python -m venv .venv
```

</td><td>

```bash
python3 -m venv .venv
```

</td></tr>
</table>

### 3. Activar el entorno virtual

<table>
<tr><th>Windows (PowerShell)</th><th>macOS / Linux</th></tr>
<tr><td>

```powershell
.venv\Scripts\Activate.ps1
```

</td><td>

```bash
source .venv/bin/activate
```

</td></tr>
</table>

Al activarlo, el prompt de la terminal empieza con `(.venv)`.

> **Windows — si aparece el error "la ejecución de scripts está deshabilitada
> en este sistema"**, ejecutar primero este comando (solo afecta a la terminal
> actual) y volver a activar:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .venv\Scripts\Activate.ps1
> ```
>
> Si se usa **CMD** en lugar de PowerShell, activar con:
> `.venv\Scripts\activate.bat`

### 4. Instalar los requerimientos

Con el entorno virtual activado (igual en todos los sistemas):

```bash
pip install -r requirements.txt
```

> En Windows, `uvloop` no está soportado; en `requirements.txt` tiene un
> marcador (`sys_platform != "win32"`) para que se omita automáticamente y la
> instalación no falle.

### 5. Ejecutar la aplicación

Con el entorno virtual activado (igual en todos los sistemas):

```bash
fastapi dev main.py
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación
interactiva en `http://127.0.0.1:8000/docs`.

Para detener el servidor: `Ctrl + C`.

> Si el comando `fastapi` no se reconoce, usar la alternativa equivalente:
> `python -m fastapi dev main.py` (Windows) o
> `python3 -m fastapi dev main.py` (macOS / Linux).

> **Windows — si aparece `UnicodeEncodeError: 'charmap' codec can't encode
> characters`** (pasa en algunas consolas que no usan UTF-8, por los emojis que
> imprime `fastapi`), forzar UTF-8 en la terminal y volver a ejecutar:
>
> ```powershell
> $env:PYTHONUTF8="1"
> fastapi dev main.py
> ```

### Resumen rápido

<table>
<tr><th>Windows (PowerShell)</th><th>macOS / Linux</th></tr>
<tr><td>

```powershell
cd TP1ProgramacionIV
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```

</td><td>

```bash
cd TP1ProgramacionIV
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

</td></tr>
</table>

---

## Probar los endpoints desde Swagger (`/docs`)

1. Con la aplicación corriendo, abrir <http://127.0.0.1:8000/docs> en el navegador.
2. Los endpoints aparecen agrupados en **users** y **components**.
3. Desplegar un endpoint → **Try it out** → completar parámetros o body →
   **Execute**.
4. Abajo se ve la respuesta (código HTTP y JSON).

Los datos se guardan **en memoria**: cada vez que se reinicia la aplicación se
vuelve a los datos de ejemplo iniciales.

---

## Parte 1 — Usuarios (`/user`)

Campos de `User`: `id` (int), `name` (str), `is_active` (bool, por defecto `true`).

| Método   | Ruta          | Descripción                                                         |
|----------|---------------|---------------------------------------------------------------------|
| `GET`    | `/user`       | Lista usuarios. Filtro opcional `?is_active=true` / `?is_active=false` (sin filtro: todos). |
| `GET`    | `/user/{id}`  | Obtiene un usuario por id (404 si no existe).                       |
| `POST`   | `/user`       | Crea un usuario (409 si el id ya existe).                           |
| `PUT`    | `/user/{id}`  | Modifica todos los datos del usuario (`name`, `is_active`).         |
| `PATCH`  | `/user/{id}`  | Modifica solo los campos enviados.                                  |
| `DELETE` | `/user/{id}`  | Elimina un usuario por id (404 si no existe).                       |

Ejemplo de body para `POST /user`:

```json
{ "id": 3, "name": "ana gomez", "is_active": false }
```

Ejemplo de body para `PUT /user/3`:

```json
{ "name": "ana maria gomez", "is_active": true }
```

Ejemplo de body para `PATCH /user/1`:

```json
{ "is_active": false }
```

---

## Parte 2 — Componentes de PC (`/component`)

Entidad propia `Component` con 5 campos:

| Campo      | Tipo   | Descripción                                    |
|------------|--------|------------------------------------------------|
| `id`       | int    | Identificador único.                           |
| `name`     | str    | Modelo del componente (ej: `"Ryzen 5 5600X"`). |
| `brand`    | str    | Marca (ej: `"AMD"`).                           |
| `category` | enum   | Tipo de componente (ver valores abajo).        |
| `price`    | float  | Precio en dólares (debe ser mayor a 0).        |

Valores válidos de `category`: `procesador`, `placa_de_video`, `memoria_ram`,
`motherboard`, `almacenamiento`, `fuente`, `gabinete`, `refrigeracion`.

| Método   | Ruta               | Descripción                                             |
|----------|--------------------|---------------------------------------------------------|
| `GET`    | `/component`       | Lista componentes. Filtros opcionales y combinables: `category` (exacta), `brand` (exacta, sin distinguir mayúsculas), `name` (contiene, sin distinguir mayúsculas), `min_price` y `max_price` (rango de precio). |
| `GET`    | `/component/{id}`  | Obtiene un componente por id (404 si no existe).        |
| `POST`   | `/component`       | Crea un componente (409 si el id ya existe).            |
| `PUT`    | `/component/{id}`  | Modifica todos los datos del componente.                |
| `PATCH`  | `/component/{id}`  | Modifica solo los campos enviados.                      |
| `DELETE` | `/component/{id}`  | Elimina un componente por id (404 si no existe).        |

Ejemplos de búsqueda:

```
GET /component?category=procesador
GET /component?brand=amd
GET /component?name=rtx
GET /component?min_price=100&max_price=200
GET /component?category=procesador&max_price=140
```

Ejemplo de body para `POST /component`:

```json
{
  "id": 5,
  "name": "B550M Aorus Elite",
  "brand": "Gigabyte",
  "category": "motherboard",
  "price": 120.5
}
```

Ejemplo de body para `PATCH /component/3`:

```json
{ "price": 280 }
```

---

## Estructura del proyecto

```
TP1ProgramacionIV/
├── main.py                # app FastAPI y registro de routers
├── requirements.txt       # dependencias
├── models/
│   ├── users.py           # modelos Pydantic de usuarios
│   └── components.py      # modelos Pydantic de componentes de PC
└── routers/
    ├── users.py           # endpoints /user
    └── components.py      # endpoints /component
```

---

## Lint y chequeo de tipos

El proyecto incluye configuración local para dos herramientas:

- **[`setup.cfg`](./setup.cfg)**: configuración de [`pycodestyle`](https://pycodestyle.pycqa.org/) (chequeo de estilo PEP 8). Define `max-line-length = 79` y excluye `.venv` y `__pycache__` del análisis.
- **[`pyrightconfig.json`](./pyrightconfig.json)**: configuración de [`pyright`](https://microsoft.github.io/pyright/) (chequeo de tipos). Apunta al entorno virtual local (`.venv`) para resolver las dependencias instaladas y excluye `.venv` y `__pycache__`.

`pyright` ya está incluido en `requirements.txt`. `pycodestyle` no, así que hay que instalarlo aparte.

Con el entorno virtual activado, correr:

```bash
pip install pycodestyle
python -m pycodestyle .
```

```bash
pyright
```
