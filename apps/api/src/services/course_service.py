from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, select, cast, String
from typing import List, Optional, Dict
from ..models import Course, prerequisite_table
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
        
        if semester:
            query = query.filter(cast(Course.semester, String).contains(semester))
        
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
        course_data = course.model_dump(exclude={'prerequisite_ids'})
        
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
        update_data = course_update.model_dump(exclude={'prerequisite_ids'}, exclude_unset=True)
        
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

        # Load prerequisite types from the association table
        prereq_rows = db.execute(select(prerequisite_table)).fetchall()
        prereq_type_map = {}
        for row in prereq_rows:
            prereq_type_map[(row.course_id, row.prerequisite_id)] = row.type or "mandatory"

        # Build dependency graph
        nodes = []
        edges = []
        visited = set()

        def add_course_to_graph(current_course, depth=0):
            if current_course.id in visited or depth > 3:
                return

            visited.add(current_course.id)

            nodes.append({
                "id": current_course.id,
                "label": current_course.title,
                "department": current_course.department,
                "credits": current_course.credits,
                "level": current_course.level
            })

            for prereq in current_course.prerequisites:
                if prereq.id not in visited:
                    add_course_to_graph(prereq, depth + 1)

                edge_type = prereq_type_map.get(
                    (current_course.id, prereq.id), "mandatory"
                )
                edges.append({
                    "source": prereq.id,
                    "target": current_course.id,
                    "type": edge_type
                })

        add_course_to_graph(course)

        # total_prerequisite_count = all nodes except the root
        total_prerequisite_count = len(nodes) - 1 if nodes else 0

        return {
            "nodes": nodes,
            "edges": edges,
            "total_prerequisite_count": total_prerequisite_count
        }

    @staticmethod
    def get_all_prerequisite_counts(db: Session) -> Dict[str, int]:
        """Get transitive prerequisite counts for all courses"""
        courses = db.query(Course).options(joinedload(Course.prerequisites)).filter(Course.is_active).all()

        # Build adjacency list: course_id -> list of direct prerequisite ids
        adj: Dict[str, List[str]] = {}
        for course in courses:
            adj[course.id] = [p.id for p in course.prerequisites]

        # Memoized DFS to count transitive prerequisites
        cache: Dict[str, int] = {}

        def count_transitive(course_id: str, visiting: set) -> int:
            if course_id in cache:
                return cache[course_id]
            if course_id in visiting:
                return 0  # cycle guard

            visiting.add(course_id)
            total = set()
            for prereq_id in adj.get(course_id, []):
                total.add(prereq_id)
                # Add all transitive prerequisites of this prereq
                _count_transitive_set(prereq_id, total, visiting)
            visiting.discard(course_id)

            cache[course_id] = len(total)
            return len(total)

        def _count_transitive_set(course_id: str, result: set, visiting: set):
            if course_id in visiting:
                return
            visiting.add(course_id)
            for prereq_id in adj.get(course_id, []):
                result.add(prereq_id)
                _count_transitive_set(prereq_id, result, visiting)
            visiting.discard(course_id)

        counts = {}
        for course in courses:
            counts[course.id] = count_transitive(course.id, set())

        return counts