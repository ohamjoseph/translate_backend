from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import auth_routes, user_routes, roles_routes, feedback_route
from src.core.database import Base, engine

from src.models import user, roles, permission, language

# Crée les tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (modifiez selon vos besoins)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
#
# app.include_router(router, prefix="/translate", tags=["translate"])


app.include_router(user_routes.router)
app.include_router(auth_routes.router)

app.include_router(roles_routes.router)

app.include_router(feedback_route.router)

