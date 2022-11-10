CREATE TABLE tracks_albums (
    track_id VARCHAR(25) REFERENCES tracks (id),
    album_id VARCHAR(25) REFERENCES albums (id),
    PRIMARY KEY (track_id, album_id)
)