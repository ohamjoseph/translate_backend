from fastapi import FastAPI
from huggingface_hub.commands import user
from starlette.middleware.cors import CORSMiddleware

from translation.route import router

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

app.include_router(router, prefix="/translate", tags=["translate"])
