from typing import Union

import spotipy
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth

app = FastAPI()

scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


@app.get("/login")
def login():
    return RedirectResponse(sp.auth_manager.get_authorize_url())


def code_param(code: str):
    return code


@app.get("/code/")
def read_code(code: str = Depends(code_param)):
    sp.auth_manager.get_access_token(code=code)
    return RedirectResponse("/")


@app.get("/")
def read_root():
    return sp.current_playback()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
