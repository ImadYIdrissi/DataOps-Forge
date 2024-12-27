import time
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "The current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


class ModelName(str, Enum):
    """Machine learning models."""

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file_from_path(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/users/{user_id}/establishment/{establishment_id}/")
async def read_user_item(
    user_id: str,
    establishment_id: str,
    desc: str,
    short: bool,
    skip: int = 0,
    limit: int = 10,
):
    desc = desc if short else f"Instead of short desc {desc} Some very long description that goes on and on and on"
    user_info = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "desc": desc,
        "items": fake_items_db[skip : skip + limit],
    }
    return user_info


class Purchase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/purchase/")
async def create_item(purchase: Purchase):
    return purchase


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


commonDeps = Annotated[dict, Depends(common_parameters)]  # type of dependency, actual declaration of dependency


@app.get("/shmushes/")
async def read_smushes(commons: commonDeps):
    return commons


@app.get("/shmooleys/")
async def read_shmooleys(commons: commonDeps):
    return commons
