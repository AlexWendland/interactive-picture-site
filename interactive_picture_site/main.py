import asyncio
import contextlib
import os
import typing

import fastapi
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
    app.state.current_points = []
    app.state.background_task = asyncio.create_task(update_image())
    yield


async def update_image():
    current_index = 0
    while True:
        current_index = (current_index + 1) % len(IMAGES)
        app.state.current_image = IMAGES[current_index]
        for client in app.state.clients:
            await client.send_text(app.state.current_image)
        await asyncio.sleep(REFRESH_RATE)


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
    await client_websocket.send_text(app.state.current_image)
    for point in app.state.current_points:
        await client_websocket.send_text(point)
    try:
        while True:
            data = await client_websocket.receive_text()
            app.state.current_points.append(data)
            for client in app.state.clients:
                if client != client_websocket:
                    await client.send_text(data)
    except Exception:
        app.state.clients.remove(client_websocket)
