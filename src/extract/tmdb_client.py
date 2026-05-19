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

    def _make_request(self,endpoint: str,params: Optional[Dict] = None) -> Optional[Dict]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, requests.HTTPError) as e:
            logger.error(f"Request failed: endpoint={endpoint}, params={params}, error={e}")
            return None

    def fetch_popular_movies(self,page:int = 1) -> Optional[Dict]:
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/popular", params)
        if data: 
            result = data.get("results", [])
            logger.info(f"Fetched {len(result)} popular movies from page {page}")
            return result
        return []
    def fetch_top_rated_movies(self, page:int = 1) -> Optional[Dict]:
        params = {
            "language": self.language,
            "page": page
        }
        data = self._make_request("movie/top_rated", params)
        if data: 
            result = data.get("results", [])
            logger.info(f"Fetched {len(result)} top rated movies from page {page}")
            return result
        return []