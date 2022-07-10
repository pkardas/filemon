from threading import Thread

from fastapi import FastAPI

from src import endpoints
from src.workers import (
    collaborative_playlists,
    listening_history,
)

app = FastAPI()
app.include_router(endpoints.router)


@app.on_event("startup")
def on_startup():
    Thread(target=listening_history.run_loop).start()
    Thread(target=collaborative_playlists.run_loop).start()


@app.on_event("shutdown")
def on_shutdown():
    collaborative_playlists.event.set()
    listening_history.event.set()
