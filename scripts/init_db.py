
from pathlib import Path
from src.database.connection import DatabaseConnection, get_db
import logging

logger = logging.getLogger(__name__)

def execute_sql_file(db: DatabaseConnection, file_path: Path):
    if not file_path.exists():
        logger.error(f"SQL file not found: {file_path}")
        return
    with open(file_path, 'r') as f:
        sql = f.read()
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for statement in statements:
            try:
                db.execute(statement)
                logger.info(f"Executed SQL statement: {statement[:30]}...")
            except Exception as e:
                logger.error(f"Error executing SQL statement: {e}")
                raise
def init_database():
    schema_dir = Path(__file__).parent.parent / 'src' / 'database' / 'schema'
    db = get_db()
    try:
        db.connect()
        sql_files = [
            "create_table.sql",
            "create_index.sql",
            "create_view.sql",
        ]
        for sql_file in sql_files:
            file_path = schema_dir / sql_file
            logger.info(f"Executing SQL file: {file_path}")
            execute_sql_file(db, file_path)
        tables = db.fetch_all("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        logger.info(f"Database initialized with tables: {[t['table_name'] for t in tables]}")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database()