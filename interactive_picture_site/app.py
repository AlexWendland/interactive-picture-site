import os
from threading import Timer

import websockets
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

IMAGE_FOLDER = "static/images"
INDEX = "static/index.html"
images = [
    picture
    for picture in os.listdir(IMAGE_FOLDER)
    if picture.endswith(("jpg", "png", "jpeg", "gif"))
]
current_index = 0
clients: list[WebSocket] = []
REFRESH_RATE = 5.0


async def update_image():
    global current_index
    current_index = (current_index + 1) % len(images)
    for client in clients:
        await client.send_text(images[current_index])
    Timer(REFRESH_RATE, update_image).start()


Timer(REFRESH_RATE, update_image).start()


@app.get("/")
async def get() -> HTMLResponse:
    with open(INDEX) as index_page:
        return HTMLResponse(index_page.read())


@app.websocket("/ws")
async def websocket_endpoint(client_websocket: WebSocket):
    await client_websocket.accept()
    clients.append(client_websocket)
    try:
        while True:
            data = await client_websocket.receive_text()
            for client in clients:
                if client != client_websocket:
                    await client.send_text(data)
    except (
        websockets.exceptions.ConnectionClosedError,
        websockets.exceptions.ConnectionClosedOK,
    ):
        clients.remove(client_websocket)
