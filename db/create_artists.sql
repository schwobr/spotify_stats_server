CREATE TABLE artists (
    id VARCHAR(25) PRIMARY KEY,
    name TEXT,
    popularity SMALLINT CHECK (popularity >= 0 AND popularity >= 100),
    genres text[]
);