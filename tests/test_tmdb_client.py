from src.extractors.tmdb_client import TMDBClient

def test_tmdb_request():
    client = TMDBClient()
    popular_movies = client.fetch_popular_movies(page=1)
    if popular_movies is not None:
        print(f"Fetched {len(popular_movies)} popular movies. \nFirst movie: {popular_movies[0]['title'] if popular_movies else 'No movies found'}")
        return True
    else:
        print("Failed to fetch popular movies.")
        return False

if __name__ == "__main__":
    test_tmdb_request()