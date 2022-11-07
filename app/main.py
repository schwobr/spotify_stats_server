from time import sleep

import spotipy
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth


class Listener:
    def __init__(self):
        self.listening = False
        self.currently_played = None


listener = Listener()
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
    return listener.currently_played


def check_currently_played():
    while listener.listening:
        listener.currently_played = sp.current_playback()
        sleep(1)
    listener.currently_played = None


@app.get("/on")
def start_listening(background_tasks: BackgroundTasks):
    listener.listening = True
    background_tasks.add_task(check_currently_played)
    return RedirectResponse("/status")


@app.get("/off")
def stop_listening():
    listener.listening = False
    return RedirectResponse("/status")


@app.get("/status")
def get_status():
    status = "on" if listener.listening else "off"
    return {"status": status}
