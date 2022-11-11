CREATE OR REPLACE VIEW full_view (play_id, track_id, track_name, track_pop, duration_ms, explicit, 
             album_id, album_name, total_tracks, release_date,
             artist_id, artist_name, artist_pop, genres,
             date_time, pct_played)
    AS SELECT p.id play_id, p.track_id track_id, t.name track_name, t.popularity track_pop, duration_ms, explicit,
              alb.id album_id, alb.name album_name, total_tracks, release_date,
              art.id artist_id, art.name artist_name, art.popularity artist_pop, genres,
              date_time, pct_played
    FROM plays p
    INNER JOIN tracks t
    ON p.track_id = t.id
    INNER JOIN tracks_artists
    ON tracks_artists.track_id = p.track_id
    INNER JOIN artists art
    ON tracks_artists.artist_id = art.id
    INNER JOIN tracks_albums
    ON tracks_albums.track_id = p.track_id
    INNER JOIN albums alb
    ON tracks_albums.album_id = alb.id;