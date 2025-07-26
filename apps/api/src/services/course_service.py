
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional
from ..models import Course
from ..schemas import CourseCreate, CourseUpdate
from fastapi import HTTPException

class CourseService:
    @staticmethod
    def get_course(db: Session, course_id: str) -> Optional[Course]:
        return db.query(Course).filter(
            Course.id == course_id,
            Course.is_active
        ).first()
    
    @staticmethod
    def get_courses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        department: Optional[str] = None,
        level: Optional[str] = None,
        language: Optional[str] = None,
        semester: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Course]:
        # Base query
        query = db.query(Course).filter(Course.is_active)

        # Check filters
        if department:
            query = query.filter(Course.department == department)
        if level:
            query = query.filter(Course.level == level)
        if language:
            query = query.filter(Course.language == language)

        if semester:
            query = query.filter(Course.semester.contains([semester]))
        
        # Search implementation for courses
        if search:
            search_term = f"%{search}"
            query = query.filter(
                or_( # or_: matches any of these fields
                    Course.id.ilike(search_term), # ilike: case-insensitive
                    Course.title.ilike(search_term),
                    Course.title_english.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
        
        query = query.order_by(Course.id)

        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_course(db: Session, course: CourseCreate) -> Course:
        # Check if course already exists
        if CourseService.get_course(db, course.id):
            raise HTTPException(status_code=400, detail="Course already exist")

        # Create course without prereqs first
        course_data = course.dict(exclude={'prerequisite_ids'})
        db_course = Course(**course_data)

        # Add prereqs
        if course.prerequisite_ids:
            prerequisites = db.query(Course).filter(
                Course.id.in_(course.prerequisite_ids)
            ).all()
            db_course.prerequisites = prerequisites
        
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    
    @staticmethod
    def update_course(db: Session, course_id: str, course_update: CourseUpdate) -> Course:
    
        db_course = CourseService.get_course(db, course_id)
        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Update fields
        update_data = course_update.dict(exclude_unset=True, exclude={'prerequisite_ids'})
        for field, value in update_data.items():
            setattr(db_course, field, value)
        
        # Update prerequisites if provided
        if course_update.prerequisite_ids is not None:
            prerequisites = db.query(Course).filter(
                Course.id.in_(course_update.prerequisite_ids)
            ).all()
            db_course.prerequisites = prerequisites
        
        db.commit()
        db.refresh(db_course)
        return db_course
        
    @staticmethod
    def get_course_dependencies(db: Session, course_id: str) -> dict:
        """Get course with all its prerequisites as a graph structure"""
        course = db.query(Course).options(
            joinedload(Course.prerequisites)
        ).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Build dependency graph
        nodes = []
        edges = []
        visited = set()

        # Starts with given course IN2040, finds prereq IN1010, then finds prereq of that: IN1000, recursively
        def add_node_and_prereqs(course, depth=0):
            if course.id in visited or depth > 3:  # Limit depth
                return
            
            visited.add(course.id)
            
            # Add node
            nodes.append({
                "id": course.id,
                "label": f"{course.id}\n{course.title}",
                "title": course.title,
                "credits": course.credits,
                "department": course.department,
                "level": course.level.value,
                "depth": depth
            })
            
            # Add edges and recursive prerequisites
            for prereq in course.prerequisites:
                edges.append({
                    "source": prereq.id,
                    "target": course.id,
                    "type": "prerequisite"
                })
                add_node_and_prereqs(prereq, depth + 1)
        
        add_node_and_prereqs(course)
        
        return {
            "course": course.id,
            "nodes": nodes,
            "edges": edges
        }