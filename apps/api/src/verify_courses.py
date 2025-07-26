from database import SessionLocal
import models

def verify_courses():
    db = SessionLocal()
    
    # Count courses
    course_count = db.query(models.Course).count()
    print(f"Total courses: {course_count}")
    
    # Show courses with prerequisites
    courses_with_prereqs = db.query(models.Course).filter(
        models.Course.prerequisites.any()
    ).all()
    
    print("\nCourses with prerequisites:")
    for course in courses_with_prereqs:
        prereq_names = [p.id for p in course.prerequisites]
        print(f"- {course.id}: {course.title}")
        print(f"  Prerequisites: {', '.join(prereq_names)}")
    
    # Show course dependency chain
    print("\nDependency chain example (IN3020):")
    in3020 = db.query(models.Course).filter(models.Course.id == "IN3020").first()
    if in3020:
        print(f"IN3020 → requires → {[p.id for p in in3020.prerequisites]}")
        for prereq in in3020.prerequisites:
            if prereq.prerequisites:
                print(f"{prereq.id} → requires → {[p.id for p in prereq.prerequisites]}")
    
    db.close()

if __name__ == "__main__":
    verify_courses()