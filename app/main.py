import os
from datetime import datetime
from math import ceil
from time import sleep

import psycopg2
import spotipy
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth


class Listener:
    def __init__(self):
        self.listening = False
        self.currently_played = None
        self.period = 5
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

    def post_currently_played(self, play_id=None):
        track = self.currently_played["item"]
        album = track["album"]
        pct_played = int(
            100 * (self.currently_played["progress_ms"] / track["duration_ms"])
        )
        pct_played = ceil(pct_played / 5) * 5

        artist = track["artists"].pop(0)

        cur = self.conn.cursor()
        cur.execute("SELECT nextval(pg_get_serial_sequence('plays', 'id'));")
        play_id = play_id or cur.fetchone()[0]

        values = {
            "play_id": play_id,
            "track_id": track["id"],
            "track_name": track["name"],
            "track_pop": track["popularity"],
            "duration_ms": track["duration_ms"],
            "explicit": track["explicit"],
            "album_id": album["id"],
            "album_name": album["name"],
            "total_tracks": album["total_tracks"],
            "release_date": album["release_date"],
            "album_pop": album["popularity"],
            "artist_id": artist["id"],
            "artist_name": artist["name"],
            "artist_pop": artist["pop"],
            "genres": artist["genres"],
            "date_time": datetime.fromtimestamp(self.currently_played["timestamp"]),
            "pct_played": pct_played,
        }
        query = f"""
            INSERT INTO full_view ({','.join(values.keys())})
            VALUES ({','.join(map(lambda x: f'%({x})s'), values.keys())};
        """
        cur.execute(query, values)
        for artist in track["artists"]:
            query1 = """
                INSERT INTO artists (id, name, popularity, genres)
                VALUES (%(id)s, %(name)s, %(popularity)s, %(genres)s
                ON CONFLICT (id) DO NOTHING;"""
            query2 = """
                INSERT INTO tracks_artists (track_id, artist_id)
                VALUES (%s, %s)
                ON CONFLICT (track_id, artist_id) DO NOTHING;
            """
            cur.execute(query1, artist)
            cur.execute(query2, (track["id"], artist["id"]))
        cur.close()
        self.conn.commit()

    def update_currently_played(self, currently_played):
        if currently_played is not None:
            if self.currently_played is None:
                self.currently_played = currently_played
            elif (
                currently_played["item"]["id"] != self.currently_played["item"]["id"]
                or currently_played["progress_ms"]
                < self.currently_played["progress_ms"]
            ):
                self.post_currently_played(
                    play_id=self.check_last_row(currently_played)
                )
                self.currently_played = currently_played

    def check_last_row(self, currently_played):
        cur = self.conn.cursor()
        query = """
            SELECT id, track_id, pct_played FROM plays
            ORDER BY id DESC
            LIMIT 1;
        """
        cur.execute(query)
        ret = cur.fetchone()
        cur.close()
        if ret is not None:
            track = currently_played["item"]
            pct_played = int(
                100 * (currently_played["progress_ms"] / track["duration_ms"])
            )
            pct_played = ceil(pct_played / 5) * 5
            old_id, old_track_id, old_pct_played = ret[0]
            if old_track_id == track["id"] and old_pct_played <= pct_played:
                return old_id


listener = Listener()
app = FastAPI()

scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


@app.on_event("shutdown")
def post_and_close():
    if listener.currently_played is not None:
        listener.post_currently_played()
    listener.conn.close()


@app.get("/login")
def login():
    return RedirectResponse(sp.auth_manager.get_authorize_url())


def code_param(code: str):
    return code


@app.get("/code/")
def read_code(code: str = Depends(code_param)):
    sp.auth_manager.get_access_token(code=code)
    return RedirectResponse(app.url_path_for("read_root"))


@app.get("/")
def read_root():
    return listener.currently_played


def check_currently_played():
    while listener.listening:
        currently_played = sp.currently_playing()
        listener.update_currently_played(currently_played=currently_played)
        sleep(listener.period)
    listener.currently_played = None


@app.get("/on")
def start_listening(background_tasks: BackgroundTasks):
    listener.listening = True
    listener.period = 5
    background_tasks.add_task(check_currently_played)
    return RedirectResponse(app.url_path_for("get_status"))


@app.get("/off")
def stop_listening():
    listener.listening = False
    return RedirectResponse(app.url_path_for("get_status"))


@app.get("/status")
def get_status():
    status = "on" if listener.listening else "off"
    return {"status": status}
