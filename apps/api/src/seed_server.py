"""
Standalone database seeding script for server deployment.
This script includes all models and database setup to avoid import issues.
"""

import os
import enum
from sqlalchemy import create_engine, Column, String, Integer, Text, ARRAY, Enum, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://myapp_user:password@localhost:5432/myapp_db')
SECRET_KEY = os.getenv('SECRET_KEY', 'development-secret-key')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum for course levels
class CourseLevel(str, enum.Enum):
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"

# Enum for semester
class Semester(str, enum.Enum):
    FALL = "fall"
    SPRING = "spring"

# Table for prerequisites
# Many to many relation
# Each course can be PR to many other courses,
# And each course can have many PR courses.
prerequisite_table = Table(
    'prerequisites',
    Base.metadata,
    Column('course_id', String, ForeignKey('courses.id'), primary_key=True),
    Column('prerequisite_id', String, ForeignKey('courses.id'), primary_key=True)
)

class Course(Base):
    __tablename__ = "courses"

    # index: can be searched for
    # Text: larger field of text
    # String: limited to 255 characters

    # Course-code: "IN1000"
    id = Column(String, primary_key=True, index=True)

    # Basic attributes for the course
    title = Column(String, nullable=False, index=True)
    title_english = Column(String)  # English title
    description = Column(Text)
    instructor = Column(String)
    credits = Column(Integer, nullable=False)

    # Classification
    department = Column(String, nullable=False, index=True)
    level = Column(Enum(CourseLevel), nullable=False, index=True)

    # When offered    
    semester = Column(ARRAY(Enum(Semester)), default=[])  # PostgreSQL ARRAY type
    language = Column(String, default="Norwegian")

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    prerequisites = relationship(
        "Course",
        secondary=prerequisite_table,
        primaryjoin=id == prerequisite_table.c.course_id,
        secondaryjoin=id == prerequisite_table.c.prerequisite_id,
        backref="dependent_courses"
    )

    # Additional metadata
    exam_form = Column(String)  # "Written", "Oral", "Project"
    teaching_form = Column(String)  # "Lectures", "Lectures + Lab"
    weekly_hours = Column(Integer)  # Hours per week


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
        "title": "Mekatronikk",
        "title_english": "Mechatronics",
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
        "title": "Introduksjon til språkteknologi",
        "title_english": "Introduction to Language Technology",
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
        "title": "Logiske metoder",
        "title_english": "Logical Methods",
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
        "title": "Software Engineering med prosjektarbeid",
        "title_english": "Software Engineering with Project Work",
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
        "title": "Digitalteknikk og datamaskinarkitektur",
        "title_english": "Digital Engineering and Computer Architecture",
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
        "title": "Beregninger og kompleksitet",
        "title_english": "Computations and complexity",
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
        "title": "Logikk for systemanalyse",
        "title_english": "Logic for System Analysis",
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
        "title": "Språkteknologiske metoder",
        "title_english": "Language Technology Methods",
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
        "title": "IT i organisasjoner",
        "title_english": "IT in Organizations",
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
    },
    {
        "id": "IN3130",
        "title": "Algoritmer: Design og effektivitet",
        "title_english": "Algorithms: Design and Efficiency",
        "description": "Emnet gir en gjennomgang av generelle algoritme-klasser som dynamisk programmering, heuristiske algoritmer, probabilistiske algoritmer, samt et representativt utvalg av enkeltalgoritmer som løser aktuelle problemer. Det legges vekt på effektivitetsvurdering. Videre gjennomgås teorien for NP-kompletthet og for uavgjørbarhet - problemer uten en løsningsalgoritme.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Muntlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2010"]
    },
    {
        "id": "IN3140",
        "title": "Introduksjon til robotikk",
        "title_english": "Introduction to Robotics",
        "description": "I dette emnet vil du få en introduksjon til robotikk. Du lærer om roboters mekaniske oppbygging, robotenes romlige beskrivelse og transformasjoner. Emnet tar også for seg kinematiske og inverskinematiske likninger for ulike robotsystemer, enkel reguleringsteknikk og styring av robotsystemer, samt robotteknologiens anvendelsesområder. Du vil også gjennomføre laboratorieøvinger for å lære å programmere enkle robotstyringer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 forelesningstimer per uke og mulighet for 2 timer regneøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3160",
        "title": "Digital systemkonstruksjon",
        "title_english": "Digital System Design",
        "description": "Design av avanserte digitale systemer. Dette innebærer programmerbare logikk-kretser, et maskinvaredesignspråk og design av system-on-chip (prosessor, minne og logikk på en brikke). Lab-oppgaver gir praktisk erfaring i hvordan virkelige design kan lages.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "Inntil 4 forelesningstimer per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3170",
        "title": "Microelectronics",
        "title_english": "Microelectronics",
        "description": "Integrert elektronikk er ryggraden i elektronikkrevolusjonen som startet med den første integrerte kretsen i 1958 og som for tiden er legemliggjort av smarttelefonene i alles lommer. Deres sentrale prosesseringsenheter inneholder milliarder av integrerte transistorer på noen få kvadrat-millimeter. Videre forbinder en mengde integrerte sensorgrensesnitt og antennedrivere den med den virkelige verden. Emnet gir en introduksjon til moderne elektronikk (CMOS) teknologi og fullt tilpasset integrert kretsdesign for både grunnleggende analoge og digitale kretser.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "English",
        "exam_form": "2 laboppgaver som hver teller 20% mot endelig karakter, 4 timers skriftlig digital eksamen som teller 60% mot endelig karakter",
        "teaching_form": "2 timer med forelesning og 1 time øvelser hver uke. 3 obligatoriske laboppgaver (2 timer per uke med labassistent og ellers fri tilgang til laben)",
        "weekly_hours": 5,
        "prerequisite_ids": ["IN1080"]
    },
    {
        "id": "IN3190",
        "title": "Digital signalbehandling",
        "title_english": "Digital Signal Processing",
        "description": "Digital signalbehandling er en sentral drivkraft i den raske utviklingen av nye metoder innen områder som telekommunikasjon (mobiltelefoni), multimedia (MP3), medisin (ultralyd), sonar, seismikk, fjernanalyse og måleteknikk. Signalbehandling kan defineres som det matematiske verktøyet som brukes for å analysere, modellere og utføre operasjoner på fysiske signaler og deres kilder. Emnet er en innføring i basismetoder som sampling, filtrering og frekvensanalyse.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Muntlig eksamen eller 4 timers avsluttende skriftlig eksamen avhengig av antall kandidater",
        "teaching_form": "Fire timer forelesning, to timer regneverksted og to timer øvingsforelesning pr. uke",
        "weekly_hours": 8,
        "prerequisite_ids": []
    },
    {
        "id": "IN3200",
        "title": "High-Performance Computing and Numerical Projects",
        "title_english": "High-Performance Computing and Numerical Projects",
        "description": "I dette emnet vil du lære om forståelse av grunnleggende konseptene innen parallell programmering og høy-ytelses databehandling (high-performance computing), samt de mest grunnleggende kommunikasjonskommandoene i MPI og programmeringsdirektiver i OpenMP. Studentene vil få den kunnskapen de trenger for å effektivt bruke moderne data-arkitektur til å løse beregningstunge vitenskaplige problemer. Slike kunnskaper er nødvendige i alle emner innenfor datavitenskap.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "4 timer med forelesninger hver uke og 2 timer med gruppe/lab hver uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["MAT1100"]
    },
    {
        "id": "IN3030",
        "title": "Effektiv parallellprogrammering",
        "title_english": "Efficient Parallel Programming",
        "description": "Emnet vil gi kunnskap om ulik bruk av parallellitet på en flerkjernet datamaskin og særlig gi innsikt i hvordan og når man i Java kan utvikle parallelle programmer som kan bli klart raskere eller enklere enn et sekvensielt program som løser det samme problemet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "English",
        "exam_form": "4 timer skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer øvelser hver uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000", "IN1010"]
    },
    {
        "id": "IN3040",
        "title": "Programmeringsspråk",
        "title_english": "Programming Languages",
        "description": "I dette emnet diskuterer vi syntaks og semantikk for programmeringsspråk generelt, inkludert statiske og dynamiske aspekter, typer og type-inferens, høyere-ordens funksjoner, polymorfisme, implementasjon og kjøretidssystemer. Vi kommer også innom forskjellige klasser av programmeringsspråk, slik som objektorienterte, funksjonelle, dynamiske og logiske språk, og vi diskuterer disse i relasjon til hverandre.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Avsluttende 4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer gruppeøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3060",
        "title": "Semantiske teknologier",
        "title_english": "Semantic Technologies",
        "description": "\"Semantic Web\" (SW) er en spennende ny utvikling for fremtidens WWW. Samtidig brukes metodene og standardene utviklet for SW i økende grad for å utveksle og integrere data i industri og offentlig sektor. Semantiske teknologier utgjør en fascinerende kombinasjon av web-teknologi, databaseteknologi, modellering, formell logikk, og kunstig intelligens.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "English",
        "exam_form": "4 timers skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN3070",
        "title": "Logikk",
        "title_english": "Logic",
        "description": "Dette er et videregående emne i logikk. Emnet fokuserer på sammenhengen mellom sannhet og bevisbarhet, og går gjennom mange grunnleggende begreper. Flere anvendelser av logikk innen informatikk blir gjennomgått.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "English",
        "exam_form": "4 timer skriftlig digital eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN3090",
        "title": "Prosjektoppgave i informatikk: Digital økonomi og ledelse",
        "title_english": "Project Assignment in Informatics: Digital Economy and Leadership",
        "description": "I dette emnet vil studenten sammen med en veileder utforske og rapportere om et tema innen digital økonomi og ledelse. Oppgaven som skal utføres vil vanligvis ha en praktisk del der studenten skal innhente data hos en organisasjon og lage en selvstendig analyse.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring", "fall"],
        "language": "Norwegian",
        "exam_form": "Vurdering av skriftlig rapport med muntlig presentasjon",
        "teaching_form": "Felles oppstartsmøte og jevnlige veiledningsmøter",
        "weekly_hours": None,
        "prerequisite_ids": ["INEC1810", "INEC1821", "INEC1831", "ECON1210"]
    },
    {
        "id": "IN3120",
        "title": "Søketeknologi",
        "title_english": "Search Technology",
        "description": "Emnet gir en innføring i teknologier for søk og informasjonsgjenfinning i stor skala over tekst. Du vil få en presentasjon av indeksstrukturer, relevans og ranking av dokumenter, samt prosessering av dokumenter og spørringer. Utvalgte anvendelser av språkteknologi og algoritmer relevante for søk blir gjennomgått.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timer skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "MAT1100",
        "title": "Kalkulus",
        "title_english": "Calculus",
        "description": "Dette emnet er en videreføring av integral- og differensialregningen i videregående skole, men emnet går dypere ned i det teoretiske grunnlaget og videreutvikler metodene til å dekke mer kompliserte tilfeller. Emnet inneholder også innføringer i komplekse tall, rekketeori og kontinuitet. MAT1100 bygger på full fordypning i matematikk fra videregående skole og danner grunnlaget for MAT1110 – Kalkulus og lineær algebra.",
        "instructor": None,
        "credits": 10,
        "department": "Mathematics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Skriftlig eksamen midt i semesteret som teller 1/3 ved sensurering. Avsluttende skriftlig eksamen som teller 2/3 ved sensurering",
        "teaching_form": "6 timer forelesning og 2 timer gruppeundervisning hver uke",
        "weekly_hours": 8,
        "prerequisite_ids": []
    },
    {
        "id": "ECON1210",
        "title": "Mikroøkonomi 1",
        "title_english": "Microeconomics 1",
        "description": "Emnet gir en innføring i mikroøkonomiske grunnbegreper og økonomisk tankegang. Med utgangspunkt i anvendte problemstillinger gjennomgås enkel markedsteori og velferdsteori, og enkle resonnementer omkring bedrifters og forbrukeres tilpasning.",
        "instructor": None,
        "credits": 10,
        "department": "Economics",
        "level": "bachelor",
        "semester": ["spring", "fall"],
        "language": "Norwegian",
        "exam_form": "3-timers skriftlig eksamen",
        "teaching_form": "Forelesninger og seminarer",
        "weekly_hours": None,
        "prerequisite_ids": []
    },
    {
        "id": "INEC1831",
        "title": "Strategi",
        "title_english": "Strategy",
        "description": "I dette emnet lærer du om de mest sentrale teoretiske retningene innenfor strategifaget, og hvilke av disse hovedskolene som er mest hensiktsmessig å benytte for å løse ulike konkrete strategiske problemstillinger i ulike typer virksomheter eller organisasjoner. Strategifaget bygger videre på økonomi, markedsføring og organisasjonsfagene, og integrerer disse i dette strategiemnet. Emnet vil ta utgangspunkt i konkrete og relevante problemstillinger og analysere disse ved gruppearbeid og diskusjoner. Mesteparten av læringen i dette emnet skjer derfor gjennom aktiv diskusjon som krever forberedelser og klasseromsdeltakelse av den enkelte.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Prosjektoppgave gjort i grupper av 2-4 studenter (50%). Individuell muntlig presentasjon etterfulgt av spørsmål fra eksaminator og sensor (50%)",
        "teaching_form": "2 timer forelesning og 2 timer gruppeøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "INEC1821",
        "title": "Digital økonomi, organisering og ledelse",
        "title_english": "Digital Economy, Organization and Leadership",
        "description": "Digital økonomi, organisering og ledelse handler om å forstå hvordan moderne organisasjoner er bygget opp og fungerer, og hvordan ledere oppnår resultater. Gjennom emnet får du grunnleggende innsikt i organisasjons- og ledelsesteori, nye digitale organisasjonsformer, og transformasjonsledelse. Det vil gis en innføring i digital økonomi, herunder digitalisering, digitale plattformer og økosystemer. Emnet vil også ta for seg hvordan bedrifter bruker data for å ta beslutninger.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Prosjektoppgave med muntlig presentasjon, gjort i grupper av 2-4 studenter (60%). Muntlig eksamen i gruppe med individuell vurdering (40%)",
        "teaching_form": "2 timer forelesning og 2 timer gruppeøvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "INEC1810",
        "title": "Marknad, markedsføring og produktutvikling",
        "title_english": "Market, Marketing and Product Development",
        "description": "I dette emnet lærer du hvordan kunder skapes og betjenes. Hva kunden ønsker, utforming av produkter og tjenester tilpasset dette, og kommunikasjon om det som tilbys til kunder og andre interessenter - samt hvordan forholde seg til kortsiktig og langsiktig lønnsomhet i markeder. Spesiell oppmerksomhet er viet informasjonsøkonomi - hvordan kjøp og salg av informasjonsvarer - som data og programvare - skiller seg fra fysiske varer og tjenester, samt hvordan bedriften kan styre forholdet mellom produktutvikling og markedsføring ved å tilpasse kundekrav og teknologiske muligheter i en dialog.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Prosjektoppgave gjort i grupper av inntil 4 studenter (60%). 4 timers avsluttende individuell digital eksamen (40%)",
        "teaching_form": "Fire timer forelesning og inntil to timer gruppeundervisning hver uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN3220",
        "title": "Å forstå bruk før bruk",
        "title_english": "Understanding Use Before Use",
        "description": "Emnet gir en oversikt over hva interaksjonsdesignere bør vite om bruk og brukskontekst for å designe optimale og brukervennlige digitale artefakter og systemer og forstå utfordringene ved å designe for bruk. Det legges vekt på begreper og teorier, illustrert med eksempler fra hverdagsliv og forskning. Emnet skal trene studentenes forestillingevne og evne til å tenke alternativt om menneskers relasjoner til digitale artefakter og systemer på kort og lang sikt.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Muntlig gruppeeksamen med individuell karakter",
        "teaching_form": "2 timer forelesning og 2 timer øvingsgrupper pr. uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1060"]
    },
    {
        "id": "IN3230",
        "title": "Nettverk",
        "title_english": "Networks",
        "description": "Dette emnet gir en grunnleggende innføring i sentrale funksjoner i kommunikasjonssystemer, herunder adressering, ruting, flytkontroll, feilhåndtering, pålitelighet og synkronisering. Det blir gitt eksempler på hvordan disse funksjonene anvendes i dagens kommunikasjonssystemer, og mer spesifikt hvordan disse anvendes innen ulike nettverksteknologier. Sentrale arkitekturer og protokoller gjennomgås.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "En deleksamen som teller 30%, og en avsluttende eksamen som teller 70%. Den avsluttende eksamen er en 4 timers skriftlig digital eksamen eller muntlig",
        "teaching_form": "2 timer forelesning og 2 timer felles oppgaveløsning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2140"]
    },
    {
        "id": "IN3240",
        "title": "Testing av programvare",
        "title_english": "Software Testing",
        "description": "Emnet dekker fundamentale begreper innenfor testing av programvare og spesifikke områder som: testing gjennom livssyklusen til et programvaresystem, statiske teknikker for testing, testdesign teknikker, testledelse, verktøystøtte for testing, testing av brukeropplevelser, testing av tilgjengelighet, eksplorativ testing, automatisert testing, testdrevet utvikling.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "To timer forelesning og to timer gruppeundervisning pr. uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN3250",
        "title": "Prosjektoppgave i informatikk: interaksjonsdesign",
        "title_english": "Project Assignment in Informatics: Interaction Design",
        "description": "I dette emnet vil studenten sammen med veileder utforske og rapportere om et tema innen interaksjonsdesign. Oppgaven som skal utføres vil involvere design og utvikling av høyoppløselige designartefakter i samråd med sluttbrukere hvor datainnsamling, utvikling og evaluering inngår som en del av eksperimentet. Emnet egner seg for studenter som ønsker å jobbe med enten etablerte næringslivscase eller pågående forskningsprosjekter som utgangspunkt for en faglig fordypning innen interaksjonsdesign.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Vurdering av skriftlig oppgave (70%), samt muntlig presentasjon av oppgaven (30%)",
        "teaching_form": "Tre fellessamlinger á to timer og individuell veiledning",
        "weekly_hours": None,
        "prerequisite_ids": ["IN2020", "IN1060", "IN1010"]
    },
    {
        "id": "IN3260",
        "title": "Prosjektoppgave i informatikk: datakommunikasjon",
        "title_english": "Project Assignment in Informatics: Data Communication",
        "description": "I dette emnet vil studenten sammen med veileder utforske og rapportere om et tema innen datakommunikasjon. Oppgaven som skal utføres vil vanligvis ha en praktisk komponent der studenten skal programmere og evaluere et eksperiment eller en applikasjon. Emnet egner seg for studenter som kan tenke seg en dypere forståelse av en del av datakommunikasjonsfaget og/eller en forsknings- eller utviklingskarriere i datakommunikasjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring", "fall"],
        "language": "Norwegian",
        "exam_form": "Vurdering av skriftlig oppgave (70%), samt muntlig presentasjon av oppgaven (30%)",
        "teaching_form": "Tre fellessamlinger á to timer og individuell veiledning",
        "weekly_hours": None,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN3290",
        "title": "Digital teknologi og samfunn",
        "title_english": "Digital Technology and Society",
        "description": "Emnet utforsker samspillet mellom digital teknologi og samfunnet bredt forstått. Dette inkluderer forholdet mellom digital teknologi og mellommenneskelige relasjoner, politikk og demokrati, næringsliv og innovasjon, forskning og bærekraft. Sentralt for emnet er antagelsen om at digital teknologi har en klar påvirkning på våre samfunn, men at vi som individer, grupper og samfunn også uunngåelig påvirker hvilke teknologiske løsninger som utvikles og velges.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig eksamen",
        "teaching_form": "2 timer forelesning per uke",
        "weekly_hours": 2,
        "prerequisite_ids": ["IN1030"]
    },
    {
        "id": "IN3310",
        "title": "Dyp læring for bildeanalyse",
        "title_english": "Deep Learning for Image Analysis",
        "description": "Dette emnet underviser i vanlige metoder innen dyp læring anvendt på bildedata, og dekker viktige algoritmer og konsepter i dyp læring for å trene nevrale nettverk. Emnet fokuserer på veiledet læring og bildegjenkjenning, men vil også introdusere andre vanlige læringsregimer og bildeanalyseoppgaver, som bildesegmentering og objektgjenkjenning.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "English",
        "exam_form": "Skriftlig eksamen (4 timer)",
        "teaching_form": "2 timer forelesninger og 2 timer grupper per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN3370",
        "title": "Digital bildebehandling og analyse",
        "title_english": "Digital Image Processing and Analysis",
        "description": "Emnet tar for seg digitale bilder og deres egenskaper, fargemodeller og persepsjon, representasjons-metoder for digitale bilder, histogramtransformasjoner og 2-dimensjonal digital konvolusjon og filtrering, segmentering, klassifikasjon, samt bildekoding og kompresjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Avsluttende digital eksamen på 4 timer",
        "teaching_form": "2 timer forelesning og 2 timer øvelser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010", "MAT1100"]
    },
    {
        "id": "IN3210",
        "title": "Network and Communications Security",
        "title_english": "Network and Communications Security",
        "description": "Network and communications security is an important part of information security: a large portion of IT-related attacks are performed either using network connections or are directed at network infrastructures. A majority of modern systems also depend on communication over networks. This course focuses on the application of cryptographic protocols and network protection techniques to secure computer networks and communication.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "English",
        "exam_form": "4 hours written digital exam",
        "teaching_form": "2 hours of lectures per week and 2 hours of workshops per week",
        "weekly_hours": 4,
        "prerequisite_ids": []
    }
]

def clear_database():
    """Clear all data from database"""
    db = SessionLocal()
    try:
        # First, clear all prerequisite relationships
        db.execute(prerequisite_table.delete())
        print("Cleared prerequisite relationships")
        
        # Then delete all courses
        deleted_count = db.query(Course).delete()
        print(f"Deleted {deleted_count} courses")
        
        db.commit()
        print("Database cleared successfully")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

def seed_real_courses():
    """Seed database with real UiO course data - exact same functionality as original"""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Starting to seed courses...")
        
        # First, create all courses without prerequisites
        course_objects = {}
        
        for course_data in all_courses_data:
            # Check if course already exists
            existing_course = db.query(Course).filter(Course.id == course_data["id"]).first()
            if existing_course:
                print(f"Course {course_data['id']} already exists, skipping...")
                course_objects[course_data["id"]] = (existing_course, course_data.get('prerequisite_ids', []))
                continue
            
            # Extract prerequisite_ids for later processing
            prereq_ids = course_data.pop('prerequisite_ids', [])
            
            # Create course
            course = Course(**course_data)
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
                prereq_course = db.query(Course).filter(Course.id == prereq_id).first()
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
        
        total_courses = db.query(Course).filter(Course.is_active == True).count()
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

def verify_courses():
    """Verify the seeded courses - same as your verify_courses.py"""
    db = SessionLocal()
    
    try:
        # Count courses
        course_count = db.query(Course).count()
        print(f"Total courses: {course_count}")
        
        # Show courses with prerequisites
        courses_with_prereqs = db.query(Course).filter(
            Course.prerequisites.any()
        ).all()
        
        print("\nCourses with prerequisites:")
        for course in courses_with_prereqs:
            prereq_names = [p.id for p in course.prerequisites]
            print(f"- {course.id}: {course.title}")
            print(f"  Prerequisites: {', '.join(prereq_names)}")
        
        # Show course dependency chain
        print("\nDependency chain example (IN3020):")
        in3020 = db.query(Course).filter(Course.id == "IN3020").first()
        if in3020:
            print(f"IN3020 → requires → {[p.id for p in in3020.prerequisites]}")
            for prereq in in3020.prerequisites:
                if prereq.prerequisites:
                    print(f"{prereq.id} → requires → {[p.id for p in prereq.prerequisites]}")
    
    except Exception as e:
        print(f"Error verifying courses: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clear":
            print("Clearing existing data...")
            clear_database()
        elif command == "verify":
            print("Verifying courses...")
            verify_courses()
        elif command == "seed":
            print("Seeding courses...")
            seed_real_courses()
        elif command == "reset":
            print("Clearing and reseeding...")
            clear_database()
            seed_real_courses()
        else:
            print("Unknown command. Use: clear, seed, verify, or reset")
    else:
        # Default behavior - clear and seed
        print("Clearing existing data...")
        clear_database()
        print("\nSeeding with real course data...")
        seed_real_courses()