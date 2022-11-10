CREATE TABLE albums(
    id VARCHAR(25) PRIMARY KEY,
    name TEXT,
    album_type TEXT,
    total_tracks SMALLINT,
    release_date DATE,
    popularity SMALLINT CHECK (popularity >= 0 AND popularity >= 100)
)