CREATE OR REPLACE FUNCTION populate_tables() RETURNS TRIGGER AS $populate_tables$
    BEGIN
        INSERT INTO plays (track_id, date_time, pct_played) 
        VALUES (NEW.track_id, NEW.date_time, NEW.pct_played)
        ON CONFLICT (id)
        DO UPDATE SET pct_played = NEW.pct_played;

        INSERT INTO tracks (id, name, popularity, duration_ms, explicit) 
        VALUES (NEW.track_id, NEW.track_name, NEW.track_pop, NEW.duration_ms, NEW.explicit)
        ON CONFLICT (id) DO NOTHING;

        INSERT INTO tracks_artists (track_id, artist_id)
        VALUES (NEW.track_id, NEW.artist_id)
        ON CONFLICT (track_id, artist_id) DO NOTHING;

        INSERT INTO tracks_albums (track_id, album_id)
        VALUES (NEW.track_id, NEW.album_id)
        ON CONFLICT (track_id, album_id) DO NOTHING;

        INSERT INTO artists (id, name, popularity, genres)
        VALUES (NEW.artist_id, NEW.artist_name, NEW.artist_pop, NEW.genres)
        ON CONFLICT (id) DO NOTHING;

        INSERT INTO albums (id, name, popularity, total_tracks, album_type, release_date)
        VALUES (NEW.album_id, NEW.album_name, NEW.album_pop, NEW.total_tracks, NEW.album_type, NEW.release_date)
        ON CONFLICT (id) DO NOTHING;

        RETURN NULL;
    END;
$populate_tables$ LANGUAGE plpgsql;

CREATE TRIGGER populate_tables
INSTEAD OF INSERT ON full_view
FOR EACH ROW EXECUTE FUNCTION populate_tables();
