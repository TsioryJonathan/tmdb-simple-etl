# TMDB Movie Pipeline


ETL Pipeline to retrieve popular movies data from TMDB API and stock them in PostgreSQL

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
python scripts/init_database.py