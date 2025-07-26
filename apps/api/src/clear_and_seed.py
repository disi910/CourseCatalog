from database import SessionLocal, engine
import models
from seed_real_courses import seed_real_courses

def clear_database():
    """Clear all data from database"""
    db = SessionLocal()
    try:
        # Delete all courses (this will cascade to prerequisites)
        db.query(models.Course).delete()
        db.commit()
        print("Database cleared successfully")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Clearing existing data...")
    clear_database()
    
    print("\nSeeding with real course data...")
    seed_real_courses()