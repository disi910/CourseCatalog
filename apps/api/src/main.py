
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .models import Course, Base
from .schemas import CourseCreate, CourseUpdate
from .schemas import Course as CourseSchema
from .database import engine, get_db
from .services.course_service import CourseService

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IFI Course Catalog API",
    description="API for course lookup at the Institute of Informatics",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


courses = ["IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010"]

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
def health_check():
    return {"status": "healthy", "database": "connected"}

# Course endpoints
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
    courses = CourseService.get_courses(
        db, skip, limit, department, level, language, semester, search
    )
    return courses


@app.get("/courses/{course_id}", response_model=CourseSchema)
def get_course(course_id: str, db: Session = Depends(get_db)):
    """Get a specific course by ID"""
    course = CourseService.get_course(db, course_id.upper())
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses/", response_model=CourseSchema, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    return CourseService.create_course(db, course)


@app.put("/courses/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: str,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing course"""
    return CourseService.update_course(db, course_id.upper(), course)


@app.delete("/courses/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    """Soft delete a course (mark as inactive)"""
    course = CourseService.get_course(db, course_id.upper())
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.is_active = False
    db.commit()
    return {"message": "Course deleted successfully"}


@app.get("/courses/{course_id}/dependencies")
def get_course_dependencies(course_id: str, db: Session = Depends(get_db)):
    """Get course dependency graph for visualization"""
    return CourseService.get_course_dependencies(db, course_id.upper())


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