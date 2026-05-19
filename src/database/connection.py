"""
PostgreSQL database connection management
"""

import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from src.config.settings import DB_CONFIG
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """PostgreSQL connection handler"""
    
    def __init__(self):
        self.config = DB_CONFIG
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        try:
            print(f"Connecting to {self.config['dbname']} at {self.config['host']}:{self.config['port']} as {self.config['user']}")
            self.conn = psycopg.connect(**self.config)
            logger.info(f"Connected to {self.config['dbname']}")
            return self.conn
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Connection closed")
    
    @contextmanager
    def get_cursor(self, dict_cursor=False):
        """Context manager for database cursors"""
        if not self.conn or self.conn.closed:
            self.connect()
        
        if dict_cursor:
            cur = self.conn.cursor(row_factory=dict_row)
        else:
            cur = self.conn.cursor()
        
        try:
            yield cur
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error: {e}")
            raise
        finally:
            cur.close()
    
    def execute(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
    
    def fetch_all(self, query, params=None):
        """Execute query and return all results as dictionaries"""
        with self.get_cursor(dict_cursor=True) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    
    def fetch_one(self, query, params=None):
        """Execute query and return one result as dictionary"""
        with self.get_cursor(dict_cursor=True) as cur:
            cur.execute(query, params)
            return cur.fetchone()
    
    def table_exists(self, table_name):
        """Check if a table exists in the database"""
        result = self.fetch_one(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
            (table_name,)
        )
        return result['exists'] if result else False


_db_instance = None

def get_db():
    """Return singleton database connection instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
    return _db_instance