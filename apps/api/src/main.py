
from fastapi import FastAPI, HTTPException, Query, Depends, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional

from .models import Course, Base
from .schemas import CourseCreate, CourseUpdate
from .schemas import Course as CourseSchema
from .database import engine, get_db
from .services.course_service import CourseService
from .auth import require_api_key

Base.metadata.create_all(bind=engine)

COURSE_ID_PATTERN = r"^[A-Za-z]{2,4}\d{4}$"

app = FastAPI(
    title="IFI Course Catalog API",
    description="API for course lookup at the Institute of Informatics",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://didriksi.com", "http://didriksi.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_route():
    return {
        "message": "Welcome to IFI Course Catalog API",
        "endpoints": {
            "courses": "/courses",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database connection failed")


# Course endpoints (read - no auth required)
@app.get("/courses/", response_model=List[CourseSchema])
def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = None,
    level: Optional[str] = None,
    language: Optional[str] = None,
    semester: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all courses with optional filtering.

    - **department**: Filter by department (e.g., "Informatics")
    - **level**: Filter by level (bachelor, master, phd)
    - **language**: Filter by language (Norwegian, English)
    - **semester**: Filter by semester (fall, spring)
    - **search**: Search in course ID, title, or description
    """
    return CourseService.get_courses(
        db, skip, limit, department, level, language, semester, search
    )


@app.get("/courses/{course_id}", response_model=CourseSchema)
def get_course(
    course_id: str = Path(pattern=COURSE_ID_PATTERN),
    db: Session = Depends(get_db),
):
    """Get a specific course by ID"""
    course = CourseService.get_course(db, course_id.upper())
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# Course endpoints (write - API key required)
@app.post("/courses/", response_model=CourseSchema, status_code=201, dependencies=[Depends(require_api_key)])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    return CourseService.create_course(db, course)


@app.put("/courses/{course_id}", response_model=CourseSchema, dependencies=[Depends(require_api_key)])
def update_course(
    course: CourseUpdate,
    course_id: str = Path(pattern=COURSE_ID_PATTERN),
    db: Session = Depends(get_db),
):
    """Update an existing course"""
    return CourseService.update_course(db, course_id.upper(), course)


@app.delete("/courses/{course_id}", dependencies=[Depends(require_api_key)])
def delete_course(
    course_id: str = Path(pattern=COURSE_ID_PATTERN),
    db: Session = Depends(get_db),
):
    """Soft delete a course (mark as inactive)"""
    course = CourseService.get_course(db, course_id.upper())
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.is_active = False
    db.commit()
    return {"message": "Course deleted successfully"}


@app.get("/courses/{course_id}/dependencies")
def get_course_dependencies(
    course_id: str = Path(pattern=COURSE_ID_PATTERN),
    db: Session = Depends(get_db),
):
    """Get course dependency graph for visualization"""
    result = CourseService.get_course_dependencies(db, course_id.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return result


# Statistics endpoints
@app.get("/statistics/departments")
def get_department_statistics(db: Session = Depends(get_db)):
    """Get course count by department"""
    stats = db.query(
        Course.department,
        func.count(Course.id).label('count')
    ).filter(
        Course.is_active
    ).group_by(
        Course.department
    ).all()

    return [{"department": dept, "count": count} for dept, count in stats]
