"""FastAPI learning."""

import time
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello world"}


@app.get("/users/me")
async def read_user_me():
    """Get the current user's ID."""
    return {"user_id": "The current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    """Get details for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: The user's ID.
    """
    return {"user_id": user_id}


class ModelName(str, Enum):
    """Enumeration for machine learning models."""

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """Get information about a specific model.

    Args:
        model_name (ModelName): The name of the model.

    Returns:
        dict: Details about the selected model.
    """
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file_from_path(file_path: str):
    """Get details about a file based on its path.

    Args:
        file_path (str): The path of the file.

    Returns:
        dict: The file path.
    """
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """Get a list of items with pagination.

    Args:
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 10.

    Returns:
        list: A list of items.
    """
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
    """Get user and establishment details along with additional information.

    Args:
        user_id (str): The user's ID.
        establishment_id (str): The establishment's ID.
        desc (str): A description of the context.
        short (bool): Whether to return a short description.
        skip (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Maximum number of items to return. Defaults to 10.

    Returns:
        dict: User and establishment details.
    """
    desc = desc if short else f"Instead of short desc {desc} Some very long description that goes on and on and on"
    user_info = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "desc": desc,
        "items": fake_items_db[skip : skip + limit],
    }
    return user_info


class Purchase(BaseModel):
    """Represents a purchase item with optional tax and description."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/purchase/")
async def create_item(purchase: Purchase):
    """Create a new purchase item.

    Args:
        purchase (Purchase): The purchase details.

    Returns:
        Purchase: The created purchase item.
    """
    return purchase


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add a process time header to the response.

    Args:
        request (Request): The incoming HTTP request.
        call_next (function): The next middleware or route handler.

    Returns:
        Response: The HTTP response with the added header.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """Define common query parameters for multiple endpoints.

    Args:
        q (str | None, optional): A query string. Defaults to None.
        skip (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Maximum number of items to return. Defaults to 100.

    Returns:
        dict: The query parameters.
    """
    return {"q": q, "skip": skip, "limit": limit}


commonDeps = Annotated[dict, Depends(common_parameters)]


@app.get("/shmushes/")
async def read_smushes(commons: commonDeps):
    """Read shmushes with common parameters.

    Args:
        commons (dict): Common query parameters.

    Returns:
        dict: The common parameters.
    """
    return commons


@app.get("/shmooleys/")
async def read_shmooleys(commons: commonDeps):
    """Read shmooleys with common parameters.

    Args:
        commons (dict): Common query parameters.

    Returns:
        dict: The common parameters.
    """
    return commons
