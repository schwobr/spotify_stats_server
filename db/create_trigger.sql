CREATE OR REPLACE FUNCTION populate_tables() RETURNS TRIGGER AS $populate_tables$
    BEGIN
        INSERT INTO tracks (id, name, popularity, duration_ms, explicit) 
        VALUES (NEW.track_id, NEW.track_name, NEW.track_pop, NEW.duration_ms, NEW.explicit)
        ON CONFLICT (id) DO NOTHING;

        INSERT INTO artists (id, name)
        VALUES (NEW.artist_id, NEW.artist_name)
        ON CONFLICT (id) DO NOTHING;

        INSERT INTO albums (id, name, total_tracks, album_type, release_date)
        VALUES (NEW.album_id, NEW.album_name, NEW.total_tracks, NEW.album_type, NEW.release_date)
        ON CONFLICT (id) DO NOTHING;

        INSERT INTO tracks_artists (track_id, artist_id)
        VALUES (NEW.track_id, NEW.artist_id)
        ON CONFLICT (track_id, artist_id) DO NOTHING;

        INSERT INTO tracks_albums (track_id, album_id)
        VALUES (NEW.track_id, NEW.album_id)
        ON CONFLICT (track_id, album_id) DO NOTHING;

        INSERT INTO plays (id, track_id, date_time, pct_played) 
        VALUES (NEW.play_id, NEW.track_id, NEW.date_time, NEW.pct_played)
        ON CONFLICT (id)
        DO UPDATE SET pct_played = NEW.pct_played;

        RETURN NULL;
    END;
$populate_tables$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER populate_tables
INSTEAD OF INSERT ON full_view
FOR EACH ROW EXECUTE FUNCTION populate_tables();
