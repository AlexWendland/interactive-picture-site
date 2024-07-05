import asyncio
import contextlib
import os
import typing

import fastapi
import websockets
from fastapi.staticfiles import StaticFiles

IMAGE_FOLDER = "static/images"
IMAGES = [
    picture
    for picture in os.listdir(IMAGE_FOLDER)
    if picture.endswith(("jpg", "png", "jpeg", "gif"))
]
INDEX = "static/index.html"
REFRESH_RATE = 5.0


# This starts the refresh loop for the picture


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncIterator[None]:
    app.state.clients = []

    app.state.background_task = asyncio.create_task(update_image())
    yield


async def update_image():
    current_index = 0
    while True:
        await asyncio.sleep(REFRESH_RATE)
        current_index = (current_index + 1) % len(IMAGES)
        for client in app.state.clients:
            await client.send_text(IMAGES[current_index])


# This creates the FastAPI app and defines the endpoints

app = fastapi.FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get("/")
async def get() -> fastapi.responses.HTMLResponse:
    with open(INDEX) as index_page:
        return fastapi.responses.HTMLResponse(index_page.read())


@app.websocket("/ws")
async def websocket_endpoint(client_websocket: fastapi.WebSocket):
    await client_websocket.accept()
    app.state.clients.append(client_websocket)
    try:
        while True:
            data = await client_websocket.receive_text()
            for client in app.state.clients:
                if client != client_websocket:
                    await client.send_text(data)
    except (
        websockets.exceptions.ConnectionClosedError,
        websockets.exceptions.ConnectionClosedOK,
    ):
        app.state.clients.remove(client_websocket)
