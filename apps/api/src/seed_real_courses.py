from database import SessionLocal, engine
import models
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

courses_data = [
    {
        "id": "IN1000",
        "title": "Introduksjon til objektorientert programmering",
        "title_english": "Introduction to Object-oriented Programming",
        "description": "Dette emnet gir en introduksjon til programmering og gir en god basis for videre studier i informatikk. Emnet forutsetter ingen forkunnskaper i programmering. Det gir en første innføring i Python og hvordan man utvikler algoritmer, inkludert bruk av lister, filer og kommunikasjon med bruker. Det blir lagt spesiell vekt på objektorientert programmering.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall", "spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger, 2 timer seminargrupper og 2 timer lab-grupper",
        "weekly_hours": 6,
        "prerequisite_ids": [] 
    },
    {
        "id": "IN1020",
        "title": "Introduksjon til datateknologi",
        "title_english": "Introduction to Computer Technology",
        "description": "Et grunnlag for utdanning i informatikk er en forståelse av hva en datamaskin er og hvordan den fungerer. Dette emnet gir denne forståelsen. Det tar for seg hvilke elementer en moderne datamaskin består av og hva de kan gjøre, og hvordan kombinasjonen av dem gir et kraftig verktøy.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN1010",
        "title": "Objektorientert programmering",
        "title_english": "Object-oriented Programming",
        "description": "Emnet er en fortsettelse av IN1000 og går dypere inn på objektorientert programmering; arbeidsspråket er Java og det blir gitt en innføring i det. Emnet tar også opp noen nyttige datastrukturer og algoritmer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Skriftlig digital midtveiseksamen (2 t) teller 25%, 4 timer skriftlig digital eksamen teller 75%",
        "teaching_form": "2 timer forelesninger, 2 timer plenumsundervisning, 2 timer gruppeundervisning",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN2010",
        "title": "Algoritmer og datastrukturer",
        "title_english": "Algorithms and Data Structures",
        "description": "Dette emnet gir en innføring i grunnleggende algoritmer og datastrukturer. Det legges vekt på å forstå hvordan en rekke sentrale algoritmer og datastrukturer fungerer, samt å kunne resonnere rundt deres kjøretidseffektivitet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 4 timer seminargrupper",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN2090",
        "title": "Databaser og datamodellering",
        "title_english": "Databases and Data Modeling",
        "description": "Dette emnet gir en grundig innføring i en metode for semantisk datamodellering og hvordan en slik modell kan realiseres som en fysisk database. Emnet gir inngående trening i bruk av SQL til å formulere spørringer mot relasjonsdatabaser.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "4 timer forelesninger/plenum og 2 timer gruppeundervising",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN3050",
        "title": "Introduksjon til kunstig intelligens og maskinlæring",
        "title_english": "Introduction to Artificial Intelligence and Machine Learning",
        "description": "Dette emnet gir en grunnleggende introduksjon til maskinlæring (ML) og kunstig intelligens (AI). Med en algoritmisk tilnærming gis studentene en praktisk forståelse av metodene som gjennomgås, ikke minst gjennom egen implementering av flere av metodene.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "English",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeøvelser",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3020",
        "title": "Databasesystemer",
        "title_english": "Database Systems",
        "description": "Emnet handler om databasesystemer, med fokus på relasjonsdatabaser, og dekker avansert bruk av slike systemer, herunder avansert SQL, optimisering av SQL-spørringer, og indeksbruk. I tillegg inneholder emnet en grundig gjennomgang av databasesystemers arkitektur, oppbygning og implementasjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "English",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "4 timer forelesning og 2 timer øvelser",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN2090"]
    }
]


def seed_real_courses():
    """Seed database with real UiO course data"""
    db = SessionLocal()
    
    try:
        # Check if courses already exist
        existing_courses = db.query(models.Course).count()
        if existing_courses > 0:
            print(f"Database already contains {existing_courses} courses. Skipping seed.")
            return
        
        # First, create all courses without prerequisites
        course_objects = {}
        for course_data in courses_data:
            # Extract prerequisite_ids for later
            prereq_ids = course_data.pop('prerequisite_ids', [])
            
            # Create course
            course = models.Course(**course_data)
            db.add(course)
            course_objects[course.id] = (course, prereq_ids)
        
        # Commit to save courses
        db.commit()
        print(f"Created {len(courses_data)} courses")
        
        # Now add prerequisites
        for course_id, (course, prereq_ids) in course_objects.items():
            for prereq_id in prereq_ids:
                if prereq_id in course_objects:
                    prereq_course = course_objects[prereq_id][0]
                    course.prerequisites.append(prereq_course)
                    print(f"Added {prereq_id} as prerequisite for {course_id}")
        
        # Commit prerequisites
        db.commit()
        print("Successfully seeded database with real UiO courses!")
        
        # Print summary
        print("\nCourse Summary:")
        for course_id, (course, prereqs) in course_objects.items():
            print(f"- {course_id}: {course.title} ({course.credits} credits)")
            if prereqs:
                print(f"  Prerequisites: {', '.join(prereqs)}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_real_courses()
