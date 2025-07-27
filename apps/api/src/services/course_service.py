from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
from ..models import Course
from ..schemas import CourseCreate, CourseUpdate

class CourseService:
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
        """
        Get courses with filtering and search functionality
        """
        # Start with base query and eagerly load prerequisites
        query = db.query(Course).options(joinedload(Course.prerequisites)).filter(Course.is_active)
        
        # Apply filters
        if department:
            query = query.filter(Course.department == department)
        
        if level:
            query = query.filter(Course.level == level)
        
        if language:
            query = query.filter(Course.language == language)
        
        # Fix semester filtering - use ANY to check if semester exists in array
        if semester:
            query = query.filter(Course.semester.any(semester))
        
        # Search functionality - search across multiple fields
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Course.id.ilike(search_term),
                    Course.title.ilike(search_term),
                    Course.title_english.ilike(search_term),
                    Course.description.ilike(search_term),
                    Course.instructor.ilike(search_term)
                )
            )
        
        # Apply pagination and return results
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_course(db: Session, course_id: str) -> Optional[Course]:
        """Get a single course by ID with prerequisites"""
        return db.query(Course).options(joinedload(Course.prerequisites)).filter(
            Course.id == course_id,
            Course.is_active
        ).first()
    
    @staticmethod
    def create_course(db: Session, course: CourseCreate) -> Course:
        """Create a new course"""
        # Extract prerequisite IDs
        prerequisite_ids = course.prerequisite_ids
        course_data = course.dict(exclude={'prerequisite_ids'})
        
        # Create course
        db_course = Course(**course_data)
        db.add(db_course)
        db.flush()  # Flush to get the ID
        
        # Add prerequisites
        if prerequisite_ids:
            prerequisites = db.query(Course).filter(Course.id.in_(prerequisite_ids)).all()
            db_course.prerequisites.extend(prerequisites)
        
        db.commit()
        db.refresh(db_course)
        return db_course
    
    @staticmethod
    def update_course(db: Session, course_id: str, course_update: CourseUpdate) -> Optional[Course]:
        """Update an existing course"""
        db_course = CourseService.get_course(db, course_id)
        if not db_course:
            return None
        
        # Extract prerequisite IDs if provided
        prerequisite_ids = course_update.prerequisite_ids
        update_data = course_update.dict(exclude={'prerequisite_ids'}, exclude_unset=True)
        
        # Update course fields
        for field, value in update_data.items():
            setattr(db_course, field, value)
        
        # Update prerequisites if provided
        if prerequisite_ids is not None:
            # Clear existing prerequisites
            db_course.prerequisites.clear()
            # Add new prerequisites
            if prerequisite_ids:
                prerequisites = db.query(Course).filter(Course.id.in_(prerequisite_ids)).all()
                db_course.prerequisites.extend(prerequisites)
        
        db.commit()
        db.refresh(db_course)
        return db_course
    
    @staticmethod
    def get_course_dependencies(db: Session, course_id: str):
        """Get course dependency graph for visualization"""
        course = CourseService.get_course(db, course_id)
        if not course:
            return None
        
        # Build dependency graph
        nodes = []
        edges = []
        visited = set()
        
        def add_course_to_graph(current_course, depth=0):
            if current_course.id in visited or depth > 3:  # Prevent infinite loops
                return
            
            visited.add(current_course.id)
            
            # Add current course as node
            nodes.append({
                "id": current_course.id,
                "label": current_course.title,
                "department": current_course.department,
                "credits": current_course.credits,
                "level": current_course.level
            })
            
            # Add prerequisites recursively
            for prereq in current_course.prerequisites:
                # Add prerequisite as node
                if prereq.id not in visited:
                    add_course_to_graph(prereq, depth + 1)
                
                # Add edge from prerequisite to current course
                edges.append({
                    "source": prereq.id,
                    "target": current_course.id,
                    "type": "prerequisite"
                })
        
        # Start building graph from the requested course
        add_course_to_graph(course)
        
        return {
            "nodes": nodes,
            "edges": edges
        }