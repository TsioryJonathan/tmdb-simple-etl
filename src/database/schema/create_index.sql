-- =====================================================
-- INDEXES FOR BETTER PERFORMANCE
-- =====================================================

-- Index on tmdb_id (already unique, but index helps lookups)
CREATE INDEX IF NOT EXISTS idx_movies_tmdb_id ON movies(tmdb_id);

-- Index for sorting by popularity
CREATE INDEX IF NOT EXISTS idx_movies_popularity ON movies(popularity DESC);

-- Index for filtering by release date
CREATE INDEX IF NOT EXISTS idx_movies_release_date ON movies(release_date);

-- Index for sorting by vote average (needs minimum votes)
CREATE INDEX IF NOT EXISTS idx_movies_vote_average ON movies(vote_average DESC) WHERE vote_count > 100;

-- Index for text search on title
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);

-- Index for genre search (using pipe-separated string)
CREATE INDEX IF NOT EXISTS idx_movies_genre_names ON movies(genre_names);

-- Index on fetched_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_movies_fetched_at ON movies(fetched_at);

-- Index for pipeline_logs queries
CREATE INDEX IF NOT EXISTS idx_pipeline_logs_execution_id ON pipeline_logs(execution_id);
CREATE INDEX IF NOT EXISTS idx_pipeline_logs_started_at ON pipeline_logs(started_at DESC);