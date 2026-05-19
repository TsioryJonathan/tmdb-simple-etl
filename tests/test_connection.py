from src.database.connection import get_db

def test_connection():
    db = get_db()
    db.connect()
    try:
        result = db.fetch_one("SELECT NOW() as now")
        print(f"Connection successful: {result['now']}")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()