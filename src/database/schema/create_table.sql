-- =====================================================
-- DATABASE: etl_movies
-- TABLES FOR TMDB MOVIE PIPELINE
-- =====================================================

-- =====================================================
-- 1. MOVIES TABLE (main table)
-- =====================================================
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    original_title VARCHAR(500),
    overview TEXT,
    release_date DATE,
    vote_average DECIMAL(3,1),
    vote_count INTEGER DEFAULT 0,
    popularity DECIMAL(10,2) DEFAULT 0.0,
    genre_names VARCHAR(500),
    poster_path VARCHAR(200),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE movies IS 'Main table storing movies from TMDB API';
COMMENT ON COLUMN movies.tmdb_id IS 'Unique identifier from TMDB API';
COMMENT ON COLUMN movies.genre_names IS 'Pipe-separated genre names (e.g., Action|Drama)';


-- =====================================================
-- 2. GENRES TABLE (reference table)
-- =====================================================
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

COMMENT ON TABLE genres IS 'Reference table for movie genres';
COMMENT ON COLUMN genres.id IS 'Genre ID from TMDB API';


-- =====================================================
-- 3. MOVIE_GENRES TABLE (junction table for many-to-many)
-- =====================================================
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

COMMENT ON TABLE movie_genres IS 'Junction table linking movies to their genres';


-- =====================================================
-- 4. PIPELINE_LOGS TABLE (track pipeline executions)
-- =====================================================
CREATE TABLE IF NOT EXISTS pipeline_logs (
    id SERIAL PRIMARY KEY,
    execution_id UUID DEFAULT gen_random_uuid(),
    pipeline_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('STARTED', 'SUCCESS', 'FAILED')),
    movies_fetched INTEGER DEFAULT 0,
    movies_inserted INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP
);

COMMENT ON TABLE pipeline_logs IS 'Logs for each pipeline execution';