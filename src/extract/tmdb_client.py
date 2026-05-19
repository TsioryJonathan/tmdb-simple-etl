import requests
import logging
from src.config.settings import TMDB_CONFIG
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class TMDBClient:
    def __init__(self):
        self.api_key = TMDB_CONFIG['api_key']
        self.base_url = TMDB_CONFIG['base_url']
        self.language = TMDB_CONFIG['language']
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json;charset=utf-8"
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, requests.HTTPError) as e:
            logger.error(f"Request failed: endpoint={endpoint}, params={params}, error={e}")
            return None

    def fetch_popular_movies(self, page: int = 1) -> List[Dict]:
        """Fetch popular movies - returns list of movies"""
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/popular", params)
        if data:
            results = data.get("results", [])
            logger.info(f"Fetched {len(results)} popular movies from page {page}")
            return results
        return []

    def fetch_top_rated_movies(self, page: int = 1) -> List[Dict]:
        """Fetch top rated movies - returns list of movies"""
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/top_rated", params)
        if data:
            results = data.get("results", [])
            logger.info(f"Fetched {len(results)} top rated movies from page {page}")
            return results
        return []

    def fetch_movies_now_playing(self, page: int = 1) -> List[Dict]:
        """Fetch movies currently in theaters - returns list of movies"""
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/now_playing", params)
        if data:
            results = data.get("results", [])
            logger.info(f"Fetched {len(results)} movies now playing from page {page}")
            return results
        return []

    def fetch_upcoming_movies(self, page: int = 1) -> List[Dict]:
        """Fetch upcoming movies - returns list of movies"""
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/upcoming", params)
        if data:
            results = data.get("results", [])
            logger.info(f"Fetched {len(results)} upcoming movies from page {page}")
            return results
        return []

    def fetch_genres(self) -> List[Dict]:
        """Fetch list of genres - returns list of genres"""
        params = {
            "language": self.language
        }
        data = self._make_request("genre/movie/list", params)
        if data:
            results = data.get("genres", [])
            logger.info(f"Fetched {len(results)} genres")
            return results
        return []

    def search_movies(self, query: str, page: int = 1) -> List[Dict]:
        """Search movies by keyword - returns list of movies"""
        params = {
            "language": self.language,
            "query": query,
            "page": page,
            "include_adult": True
        }
        data = self._make_request("search/movie", params)
        if data:
            results = data.get("results", [])
            logger.info(f"Fetched {len(results)} search results for query '{query}' on page {page}")
            return results
        return []

    def fetch_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Fetch details for a specific movie - returns dict or None"""
        params = {
            "language": self.language
        }
        data = self._make_request(f"movie/{movie_id}", params)
        if data:
            logger.info(f"Fetched details for movie ID {movie_id}")
            return data
        return None

    def close(self):
        """Close HTTP session"""
        self.session.close()
        logger.info("TMDB client session closed")