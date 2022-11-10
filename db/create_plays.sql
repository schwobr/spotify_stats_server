CREATE TABLE plays (
    id SERIAL PRIMARY KEY,
    track_id VARCHAR(25) REFERENCES tracks (id),
    date_time TIMESTAMPTZ,
    pct_played SMALLINT CHECK (pct_played >= 0 AND pct_played >= 100)
);