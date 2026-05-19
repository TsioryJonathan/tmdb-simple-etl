-- =====================================================
-- USEFUL VIEWS FOR ANALYTICS
-- =====================================================

-- View: Latest movies (last 30 days)
CREATE OR REPLACE VIEW recent_movies AS
SELECT 
    tmdb_id,
    title,
    release_date,
    vote_average,
    popularity,
    genre_names
FROM movies
WHERE release_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY release_date DESC;

COMMENT ON VIEW recent_movies IS 'Movies released in the last 30 days';


-- View: Top rated movies (minimum 100 votes)
CREATE OR REPLACE VIEW top_rated_movies AS
SELECT 
    tmdb_id,
    title,
    release_date,
    vote_average,
    vote_count,
    popularity,
    genre_names
FROM movies
WHERE vote_average IS NOT NULL AND vote_count >= 100
ORDER BY vote_average DESC;

COMMENT ON VIEW top_rated_movies IS 'Movies with at least 100 votes, sorted by rating';


-- View: Genre statistics
CREATE OR REPLACE VIEW genre_statistics AS
WITH genre_split AS (
    SELECT 
        tmdb_id,
        title,
        vote_average,
        unnest(string_to_array(genre_names, '|')) as genre_name
    FROM movies
    WHERE genre_names IS NOT NULL
)
SELECT 
    genre_name,
    COUNT(*) as movie_count,
    ROUND(AVG(vote_average)::numeric, 2) as avg_rating
FROM genre_split
GROUP BY genre_name
ORDER BY movie_count DESC;

COMMENT ON VIEW genre_statistics IS 'Statistics per genre: number of movies and average rating';


-- View: Movies by year
CREATE OR REPLACE VIEW yearly_statistics AS
SELECT 
    EXTRACT(YEAR FROM release_date) as year,
    COUNT(*) as movie_count,
    ROUND(AVG(vote_average)::numeric, 2) as avg_rating,
    MAX(vote_average) as highest_rating,
    MIN(vote_average) as lowest_rating
FROM movies
WHERE release_date IS NOT NULL AND vote_average IS NOT NULL
GROUP BY EXTRACT(YEAR FROM release_date)
ORDER BY year DESC;

COMMENT ON VIEW yearly_statistics IS 'Movie statistics grouped by release year';


-- View: Latest pipeline execution status
CREATE OR REPLACE VIEW latest_pipeline_status AS
SELECT 
    execution_id,
    pipeline_name,
    status,
    movies_fetched,
    movies_inserted,
    started_at,
    finished_at,
    EXTRACT(EPOCH FROM (finished_at - started_at)) as duration_seconds
FROM pipeline_logs
ORDER BY started_at DESC
LIMIT 10;

COMMENT ON VIEW latest_pipeline_status IS 'Last 10 pipeline executions with duration';