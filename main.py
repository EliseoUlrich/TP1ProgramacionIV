from fastapi import FastAPI
from routers import users, components

# Create the application instance
app = FastAPI()

# Router to user endpoints
app.include_router(users.router)

# Router to PC component endpoints (entidad propia - Parte 2 del TP)
app.include_router(components.router)


# Define a GET route for the root URL
@app.get("/")
def read_root():
    mensaje = "Primer clase de FastAPI"
    return {"message": mensaje}
