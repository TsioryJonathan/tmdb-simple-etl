from typing import List, Optional, Dict
from datetime import datetime
import logging
from src.extractors.tmdb_client import TMDBClient

logger = logging.getLogger(__name__)


class MovieTransformer:
    def __init__(self, genre_dict: Optional[Dict[int, str]] = None):
        self.genre_dict = genre_dict or {}
    
    def set_genres(self, genre_dict: List[Dict[int, str]] = None):
        if genre_dict:
            self.genre_dict = {genre["id"]: genre["name"] for genre in genre_dict}
            logger.info(f"Genre dictionary set manually with {len(genre_dict)} genres")
        else:
            tmdb_client = TMDBClient()
            try:
                genres = tmdb_client.fetch_genres()
                self.genre_dict = {genre["id"]: genre["name"] for genre in genres}
                logger.info(f"Genre dictionary fetched from API: {len(self.genre_dict)} genres")
            finally:
                tmdb_client.close()
    def get_genre_dict(self) -> Dict[int, str]:
        return self.genre_dict
    def _transform_genres(self, genre_ids: List[int]) -> Optional[str]:
        if not genre_ids:
            return None
        
        genre_names = []
        for genre_id in genre_ids:
            if genre_id not in self.genre_dict:
                logger.warning(f"Genre ID {genre_id} not found in genre dictionary")
                continue
            genre_names.append(self.genre_dict[genre_id])
        
        return "|".join(genre_names) if genre_names else None
    
    def _transform_date(self, date_str: Optional[str]) -> Optional[str]:
        if not date_str:
            return None
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError as e:
            logger.error(f"Error parsing date '{date_str}': {e}")
            return None
    
    def _truncate_text(self, text: Optional[str], max_length: int) -> Optional[str]:
        if text is None:
            return None
        return text[:max_length]
    
    def transform_movie(self, movie: Dict) -> Dict:
        if not movie.get("id"):
            logger.error("Movie ID is missing")
            raise ValueError("Movie ID is required")
        
        if not movie.get("title"):
            logger.error(f"Movie title is missing for movie ID {movie.get('id')}")
            raise ValueError("Movie title is required")
        
        transformed_movie = {
            "tmdb_id": movie.get("id"),
            "title": self._truncate_text(movie.get("title"), 500),
            "original_title": self._truncate_text(movie.get("original_title"), 500),
            "overview": self._truncate_text(movie.get("overview"), 1000),
            "release_date": self._transform_date(movie.get("release_date")),
            "popularity": movie.get("popularity"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count", 0),
            "poster_path": self._truncate_text(movie.get("poster_path"), 200),
            "genre_names": self._transform_genres(movie.get("genre_ids", []))
        }
        
        logger.debug(f"Transformed movie: {transformed_movie['tmdb_id']} - {transformed_movie['title']}")
        return transformed_movie
    
    def transform_batch(self, movies: List[Dict]) -> List[Dict]:
        if not movies:
            return []
        
        transformed_movies = []
        skipped = 0
        
        for movie in movies:
            try:
                transformed_movie = self.transform_movie(movie)
                transformed_movies.append(transformed_movie)
            except ValueError as e:
                logger.error(f"Skipping movie: {e}")
                skipped += 1
        
        logger.info(f"Transformed {len(transformed_movies)} movies, skipped {skipped}")
        return transformed_movies
    
    def get_genre_ids_from_movies(self, movies: List[Dict]) -> set:
        genre_ids = set()
        for movie in movies:
            for genre_id in movie.get("genre_ids", []):
                genre_ids.add(genre_id)
        return genre_ids


def get_movie_transformer(genre_dict: Optional[Dict[int, str]] = None) -> MovieTransformer:
    """Factory function to get MovieTransformer instance"""
    return MovieTransformer(genre_dict)