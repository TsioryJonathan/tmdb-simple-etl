from src.extractors.tmdb_client import TMDBClient
from src.transformers.movie_transformer import MovieTransformer

def test_movie_transformer():
    tmdb_client = TMDBClient()
    movies = tmdb_client.fetch_popular_movies(page=1)

    transformer = MovieTransformer()
    transformer.set_genres()

    transformed_movie = transformer.transform_batch(movies)
    [print(movie) for movie in transformed_movie]
    
if __name__ == "__main__":
    test_movie_transformer()
