from database import SessionLocal, engine
import models
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

all_courses_data = [
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
    },
    {
        "id": "IN1030",
        "title": "Systemer, krav og konsekvenser",
        "title_english": "Systems, Requirements and Consequences",
        "description": "Dette emnet gir forståelse i utvikling og bruk av digitale systemer. I den første halvdelen av emnet er fokuset på systemenes samfunnsmessige konsekvenser, brukernes aktiviteter og etikk. I den andre halvdelen tas dette videre og fokuset er på hvordan systemer utvikles sett fra et software engineerings perspektiv.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 3 timer sammenhengende gruppeundervisning per uke",
        "weekly_hours": 5,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN1050",
        "title": "Introduksjon til design, bruk, interaksjon",
        "title_english": "Introduction to Design, Use and Interaction",
        "description": "Emnet gir en introduksjon til design, bruk og interaksjon, hvor fokuset er på interaksjon og samspillet mellom mennesker og digital teknologi. Emnet tar for seg undersøkelser av bruk av teknologi. Begreper og metoder for design, prototyping og evaluering introduseres.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers digital skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer øvingsgrupper og 2 timer plenumsøvelser hver uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN1060",
        "title": "Bruksorientert design",
        "title_english": "User-oriented Design",
        "description": "I dette emnet vil du lære hvordan forståelse av brukernes behov gir grunnlag for design, og hvordan prototyper og designforslag kan gi brukerne bedre grunnlag for å formulere sine behov. Du kommer til å planlegge og gjennomføre et prosjekt hvor du skal designe og bygge en digital prototype for og med en valgt brukergruppe.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Muntlig gruppevis eksamen med individuell karaktersetting",
        "teaching_form": "2 timer forelesninger og 2 timer øvingsgrupper hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1050"]
    },
    {
        "id": "IN1080",
        "title": "Elektroniske systemer",
        "title_english": "Electronic Systems",
        "description": "Grunnleggende analog elektronikk, sensorer og sensor grensesnitt, aktuatorer. Programmering av mekatroniske systemer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN1140",
        "title": "Språkteknologi",
        "title_english": "Language Technology",
        "description": "Emnet gir en innføring i språkteknologi: metoder for automatisk analyse av språklige data. Det vil videre gi en innføring i lingvistisk teori og relatere denne til språkteknologiske problemområder.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timer skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN1150",
        "title": "Logiske metoder for informatikk",
        "title_english": "Logical Methods for Computer Science",
        "description": "Dette er et emne i grunnleggende matematiske og logiske metoder. Det legges vekt på forståelse og tilvenning av matematiske begreper og notasjon som er relevante for et studium i informatikk. EKSAMEN VIL IKKE BLI AVHOLDT I HØST 2025.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring", "fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN2000",
        "title": "Software Engineering og prosjektarbeid",
        "title_english": "Software Engineering and Project Work",
        "description": "I dette emnet skal du gjennomføre et omfattende systemutviklingsprosjekt i team, og vil få trening i å bruke moderne metoder, teknikker og verktøy innen software engineering.",
        "instructor": None,
        "credits": 20,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen og prosjektoppgave med muntlig presentasjon",
        "teaching_form": "Inntil 4 timer forelesning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010", "IN1030", "IN2010"]
    },
    {
        "id": "IN2020",
        "title": "Metoder i interaksjonsdesign",
        "title_english": "Methods in Interaction Design",
        "description": "I dette emnet lærer du om forskning i HCI (Human-Computer Interaction). Vi går gjennom forskjellige tilnærminger til design innenfor HCI-feltet, og du får inngående kunnskap om metoder, verktøy og teknikker for HCI-forskning.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer øvingsgrupper hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1050", "IN1060"]
    },
    {
        "id": "IN2031",
        "title": "Prosjektoppgave i programmering",
        "title_english": "Programming Project",
        "description": "Emnets kjerne er en større programmeringsoppgave som skal løses i små grupper. Gjennom oppgaven vil du få praktisk trening i programmering og få erfaring med hvordan objektorientert tankegang og mekanismer kan være ekstra nyttige i utviklingen av større programmer. Gjennom prosjektoppgaven vil du også få innblikk i domenespesifikke språk og lære for eksempel hvordan en kompliator eller interpret fungerer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Innlevering av prosjektoppgave basert på de obligatoriske oppgavene. Eventuell muntlig eksaminasjon.",
        "teaching_form": "2 timer forelesning annenhver uke og 2 timer øvelse hver uke",
        "weekly_hours": 3,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN2040",
        "title": "Funksjonell programmering",
        "title_english": "Functional Programming",
        "description": "Programmering i et funksjonelt programmeringsspråk. Rekursjon. Abstrakte datastrukturer. Datastyrt programmering, memoisering, objektorientering, lister og strømmer. Styrker og svakheter ved funksjonell programmering sammenlignet med imperativ programmering. Semantikk for evaluering av funksjonskall og interpretering av funksjonelle programmer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN2060",
        "title": "Digital teknologi",
        "title_english": "Digital Technology",
        "description": "Emnet tar for seg prinsipper i digital design, som kombinatorisk og sekvensiell logikk, tilstandsmaskiner og digitale byggeblokker, og bygger på dette for å introdusere prosessorarkitekturer, pipelining, cache, og grensesnittet mellom maskinvare og programkode.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN2080",
        "title": "Logikk og beregninger",
        "title_english": "Logic and Computations",
        "description": "I dette emnet lærer du om sammenhengene mellom ulike beregningsmodeller, formelle språk, deres begrensinger og kompleksitet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeøvelser per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1150"]
    },
    {
        "id": "IN2100",
        "title": "Distribuerte systemer",
        "title_english": "Distributed Systems",
        "description": "Emnet gir en høynivå innføring i distribuerte datasystemer, og viser hvordan logiske metoder kan brukes til å modellere og resonnere om datatyper og distribuerte systemer. Emnet introduserer ulike klasser av distribuerte systemer, som transport-protokoller, database-protokoller, klassiske distribuerte algoritmer og sikkerhetsprotokoller.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "6 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN2110",
        "title": "Datalingvistikk",
        "title_english": "Computational Linguistics",
        "description": "Emnet gir en fordypning i grunnleggende metoder og praktiske verktøy for basal språkteknologi (metoder for automatisk analyse av språklige data). Det dekkes både regelbaserte teknikker, f.eks. frasestrukturgrammatikk, og tilnærminger med utgangspunkt i maskinlæring, f.eks. vektorromsemantikk og klassifikasjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN2120",
        "title": "Informasjonssikkerhet",
        "title_english": "Information Security",
        "description": "Dette emnet gir en bred innføring i informasjonssikkerhet og cybersikkerhet, som grunnlag for å forstå, vurdere og anvende ulike tiltak på teknisk og organisatorisk nivå som kan gi adekvat beskyttelse av informasjonsressurser mot skade.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer øvingsgrupper hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN2140",
        "title": "Introduksjon til operativsystemer og datakommunikasjon",
        "title_english": "Introduction to Operating Systems and Data Communication",
        "description": "Emnet gir en innføring i operativsystemer, sett både fra brukerens og programmererens synspunkt, og fra maskinens side. Det vil også gi innsikt i hvordan dagens datakommunikasjon foregår og hvordan man lager programmer som benytter slik kommunikasjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Praktisk eksamen (40%) og 4 timers skriftlig eksamen (60%)",
        "teaching_form": "2 timer forelesning, 2 timer praktisk undervisning og 2 timer plenumsundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1020", "IN1000"]
    },
    {
        "id": "IN2150",
        "title": "Store og komplekse informasjonssystemer",
        "title_english": "Large and Complex Information Systems",
        "description": "I dette emnet lærer du om hvordan organisasjoner håndterer informasjonssystemer. Undervisningen er basert på at du samarbeider med eksterne organisasjoner og analyserer konkrete eksempler fra privat og offentlig sektor.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Avsluttende hjemmeeksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeseminar hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3000",
        "title": "Operativsystemer",
        "title_english": "Operating Systems",
        "description": "Dette emnet gir en grundig introduksjon til alle aspekter av prosesshåndtering i operativsystemer. Tema inkluderer avbruddsbehandling, tråder og prosesser, prosesskoordinering og synkronisering, fysisk og virtuelt lagerorganisering, ytere enheter og filsystemer.",
        "instructor": None,
        "credits": 20,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Innlevering av seks prosjektoppgaver (teoretisk og praktisk del)",
        "teaching_form": "4 timer forelesninger og 4 timer øvelser per uke",
        "weekly_hours": 8,
        "prerequisite_ids": ["IN2010"]
    },
    {
        "id": "IN3010",
        "title": "Transformativt design",
        "title_english": "Transformative Design",
        "description": "I dette emnet lærer du om transformativt design - design mot en bærekraftig fremtid. Du skal bruke kunnskap om forskjellige tilnærminger til design i et ekte prosjekt hvor du lager et designforslag i samarbeid med offentlige eller privat sektor, eller store forskningsprosjekter.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Muntlig midtveispresentasjon, muntlig sluttpresentasjon og skriftlig rapport",
        "teaching_form": "2 timer undervisning pr. uke (forelesning, diskusjon, designkritikk)",
        "weekly_hours": 2,
        "prerequisite_ids": ["IN2020"]
    },
    {
        "id": "IN3015",
        "title": "Ultralydavbildning",
        "title_english": "Ultrasound Imaging",
        "description": "Avbildning ved bruk av ultralyd benyttes innen blant annet medisin, sonar og ikke-destruktiv testing. Dette emnet forklarer de grunnleggende prinsippene for akustisk avbildning, stråleforming og avbildningsmodaliteter innen ultralyd.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timer skriftlig eller muntlig eksamen",
        "teaching_form": "Syv moduler av to ukers varighet, hver med 4 timer forelesning og 4 timer prosjektarbeid",
        "weekly_hours": 4,
        "prerequisite_ids": []
    }
]

def seed_real_courses():
    """Seed database with real UiO course data"""
    db = SessionLocal()
    
    try:
        print("Starting to seed courses...")
        
        # First, create all courses without prerequisites
        course_objects = {}
        
        for course_data in all_courses_data:
            # Check if course already exists
            existing_course = db.query(models.Course).filter(models.Course.id == course_data["id"]).first()
            if existing_course:
                print(f"Course {course_data['id']} already exists, skipping...")
                course_objects[course_data["id"]] = (existing_course, course_data.get('prerequisite_ids', []))
                continue
            
            # Extract prerequisite_ids for later processing
            prereq_ids = course_data.pop('prerequisite_ids', [])
            
            # Create course
            course = models.Course(**course_data)
            db.add(course)
            course_objects[course.id] = (course, prereq_ids)
            print(f"Created course: {course.id}")
        
        # Commit to save all courses first
        db.commit()
        print(f"Committed {len(course_objects)} courses to database")
        
        # Now add prerequisites
        print("Adding prerequisites...")
        prerequisite_count = 0
        
        for course_id, (course, prereq_ids) in course_objects.items():
            for prereq_id in prereq_ids:
                # Find the prerequisite course
                prereq_course = db.query(models.Course).filter(models.Course.id == prereq_id).first()
                if prereq_course:
                    # Check if relationship already exists
                    if prereq_course not in course.prerequisites:
                        course.prerequisites.append(prereq_course)
                        prerequisite_count += 1
                        print(f"Added {prereq_id} as prerequisite for {course_id}")
                    else:
                        print(f"Prerequisite {prereq_id} already exists for {course_id}")
                else:
                    print(f"Warning: Prerequisite course {prereq_id} not found for {course_id}")
        
        # Commit prerequisites
        db.commit()
        print(f"Successfully added {prerequisite_count} prerequisite relationships!")
        
        # Print summary
        print("\n" + "="*50)
        print("SEEDING SUMMARY")
        print("="*50)
        
        total_courses = db.query(models.Course).filter(models.Course.is_active == True).count()
        print(f"Total active courses in database: {total_courses}")
        
        print("\nCourses with prerequisites:")
        for course_id, (course, prereq_ids) in course_objects.items():
            if prereq_ids:
                # Refresh course to get updated prerequisites
                db.refresh(course)
                actual_prereqs = [p.id for p in course.prerequisites]
                print(f"- {course_id}: {course.title}")
                print(f"  Expected prerequisites: {prereq_ids}")
                print(f"  Actual prerequisites: {actual_prereqs}")
                if set(prereq_ids) != set(actual_prereqs):
                    print(f"  ⚠️  MISMATCH!")
                print()
        
        print("Seeding completed successfully! 🎉")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_real_courses()
