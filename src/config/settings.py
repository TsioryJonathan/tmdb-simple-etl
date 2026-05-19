import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

load_dotenv(ROOT_DIR / ".env")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "tmdb_movies"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

TMDB_CONFIG = {
    "api_key": os.getenv("TMDB_API_KEY", ""),
    "base_url": "https://api.themoviedb.org/3",
    "language": "en-US"
}

PIPELINE_CONFIG = {
    "default_pages": 2,         
    "movies_per_page": 20,        
    "batch_size": 100             
}

def validate_config():
    errors = []
    
    if not DB_CONFIG["password"]:
        errors.append("DB_PASSWORD not found in .env")
    
    if not TMDB_CONFIG["api_key"]:
        errors.append("TMDB_API_KEY not found in .env")
    
    if errors:
        for error in errors:
            print(error)
        return False
    
    print("Configuration is valid.")
    return True

if __name__ == "__main__":
    validate_config()