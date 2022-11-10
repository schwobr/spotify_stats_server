CREATE TABLE albums_artists (
    album_id VARCHAR(25) REFERENCES albums (id),
    artist_id VARCHAR(25) REFERENCES artists (id),
    PRIMARY KEY (album_id, artist_id)
);