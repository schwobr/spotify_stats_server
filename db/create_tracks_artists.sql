CREATE TABLE tracks_artists (
    track_id VARCHAR(25) REFERENCES tracks (id),
    artist_id VARCHAR(25) REFERENCES artists (id),
    PRIMARY KEY (track_id, artist_id)
);