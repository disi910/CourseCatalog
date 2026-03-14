"""
Database seeding script for server deployment.
Imports shared models and database configuration.
"""

import sys
import os

# Allow running as standalone script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Base, engine, SessionLocal
from src.models import Course, CourseLevel, Semester, prerequisite_table


all_courses_data = [
    {
        "id": "IN1000",
        "title": "Introduksjon til objektorientert programmering",
        "title_english": "Introduction to Object-oriented Programming",
        "description": "Dette emnet gir en introduksjon til programmering og gir en god basis for videre studier i informatikk. Emnet forutsetter ingen forkunnskaper i programmering. Det gir en f\u00f8rste innf\u00f8ring i Python og hvordan man utvikler algoritmer, inkludert bruk av lister, filer og kommunikasjon med bruker. Det blir lagt spesiell vekt p\u00e5 objektorientert programmering.",
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
        "id": "IN1010",
        "title": "Objektorientert programmering",
        "title_english": "Object-oriented Programming",
        "description": "Emnet gir en videref\u00f8ring i programmering i Java med et s\u00e6rlig fokus p\u00e5 objektorientert tankegang og teknikker: klasser og subklasser, grensesnitt, pekere og enkle datastrukturer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger, 2 timer seminargrupper og 2 timer lab-grupper",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN1020",
        "title": "Introduksjon til datateknologi",
        "title_english": "Introduction to Computer Technology",
        "description": "Emnet gir en grunnleggende innf\u00f8ring i datateknologi og datamaskiner: Bin\u00e6re tall. Kombinatorisk logikk (port-niv\u00e5). Sekvensiell logikk (flip-flop). Datamaskinens grunnleggende komponenter og arkitektur. Assemblyprogrammering for ARM. Avbrudd.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN1030",
        "title": "Systemutvikling",
        "title_english": "Systems Development",
        "description": "Emnet gir en innf\u00f8ring i aktivitetene som inng\u00e5r i utvikling av programvaresystemer og ulike m\u00e5ter \u00e5 organisere disse p\u00e5. Emnet bygger p\u00e5 kunnskap om programmering og gir en bredere forst\u00e5else for informatikk. Emnet dekker ogs\u00e5 arbeid med krav, brukersentrert design, og iterativ utviklingsmetodikk.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppearbeid per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "IN1050",
        "title": "Introduksjon til design",
        "title_english": "Introduction to Design",
        "description": "Emnet gir en innf\u00f8ring i grafisk design, designprinsipper og hvordan man designer l\u00f8sninger og tjenester som er brukervennlige. Du l\u00e6rer \u00e5 planlegge, designe og evaluere digitale l\u00f8sninger basert p\u00e5 brukernes behov.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Hjemmeeksamen",
        "teaching_form": "2 timer forelesning og 4 timer grupper per uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN1060",
        "title": "Bruksorientert design",
        "title_english": "Use-oriented Design",
        "description": "Emnet gir en innf\u00f8ring i brukersentrerte design- og utviklingsmetoder. Emnet fokuserer p\u00e5 forst\u00e5else av brukerbehov, prototyping, og evaluering av design.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Hjemmeeksamen over 3 dager",
        "teaching_form": "2 timer forelesning og 4 timer grupper per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1050"]
    },
    {
        "id": "IN1080",
        "title": "Digitalteknikk og datamaskinarkitektur",
        "title_english": "Digital Technology and Computer Architecture",
        "description": "Emnet gir en grunnleggende innf\u00f8ring i digital teknologi og datamaskinarkitektur. Bin\u00e6re tall. Kombinatorisk og sekvensiell logikk. Datamaskinens oppbygning og virkm\u00e5te.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer lab per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN1150",
        "title": "Logiske metoder",
        "title_english": "Logical Methods",
        "description": "Emnet gir en innf\u00f8ring i logisk tenkning og matematisk bevisf\u00f8ring som brukes i informatikk. Hovedtemaer inkluderer utsagnslogikk, predikatlogikk, mengdel\u00e6re, relasjoner og funksjoner.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN1900",
        "title": "Introduksjon til programmering med vitenskapelige anvendelser",
        "title_english": "Introduction to Programming with Scientific Applications",
        "description": "Emnet gir en introduksjon til programmering i Python, med vekt p\u00e5 vitenskapelige beregninger og anvendelser. Studentene l\u00e6rer grunnleggende programmering, numeriske metoder og datavisualisering.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen + obligatorisk prosjekt",
        "teaching_form": "2 timer forelesninger, 2 timer seminargrupper og 2 timer lab-grupper",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "IN1910",
        "title": "Programmering for naturvitenskaplige anvendelser",
        "title_english": "Programming for Scientific Applications",
        "description": "Emnet bygger videre p\u00e5 IN1900 med mer avanserte Python-teknikker for vitenskapelig programmering, inkludert objektorientert programmering, numeriske l\u00f8sningsmetoder og bruk av vitenskapelige Python-biblioteker.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig digital eksamen + obligatorisk prosjekt",
        "teaching_form": "2 timer forelesninger og 2 timer datalab per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1900"]
    },
    {
        "id": "IN2000",
        "title": "Software Engineering med prosjektarbeid",
        "title_english": "Software Engineering with Project Work",
        "description": "I IN2000 jobber studentene i sm\u00e5 grupper med et semesterlangt prosjekt der de utvikler en Android-applikasjon. Emnet l\u00e6rer smidige utviklingsmetoder og praktisk programvareutvikling.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Prosjektarbeid med rapport og presentasjon",
        "teaching_form": "2 timer forelesning og gruppeprosjekt per uke",
        "weekly_hours": 10,
        "prerequisite_ids": ["IN1010", "IN1030"]
    },
    {
        "id": "IN2010",
        "title": "Algoritmer og datastrukturer",
        "title_english": "Algorithms and Data Structures",
        "description": "Emnet gir en grunnleggende innf\u00f8ring i algoritmer og datastrukturer som brukes i informatikk: Lister, stakker, k\u00f8er, tr\u00e6r, grafer, s\u00f8king, sortering, og algoritmisk kompleksitet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesninger og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN2020",
        "title": "Metoder i interaksjonsdesign",
        "title_english": "Methods in Interaction Design",
        "description": "Emnet gir en innf\u00f8ring i metoder brukt i interaksjonsdesign, b\u00e5de kvalitative og kvantitative. Studentene l\u00e6rer om brukerunderst\u00f8kelser, prototyping, og evaluering av interaktive systemer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Hjemmeeksamen",
        "teaching_form": "2 timer forelesning og 4 timer grupper per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1060"]
    },
    {
        "id": "IN2040",
        "title": "Funksjonell programmering",
        "title_english": "Functional Programming",
        "description": "Emnet gir en innf\u00f8ring i funksjonell programmering og programspr\u00e5kteori ved bruk av Standard ML. Emnet dekker typesystemer, m\u00f8nstergjenkjenning, h\u00f8yere ordens funksjoner, og formell semantikk.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer grupper per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN2060",
        "title": "Digitalteknikk",
        "title_english": "Digital Technology",
        "description": "Emnet gir videref\u00f8ring i digital teknologi med vekt p\u00e5 VHDL og FPGA-programmering. Emnet tar for seg mer avanserte digitale systemer og deres implementering.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen + obligatorisk lab",
        "teaching_form": "2 timer forelesning og 4 timer lab per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1020"]
    },
    {
        "id": "IN2070",
        "title": "Datamaskinarkitektur",
        "title_english": "Computer Architecture",
        "description": "Emnet gir en innf\u00f8ring i datamaskinarkitektur, pipeline, cache, virtuelt minne og parallellisme. Emnet fokuserer p\u00e5 moderne prosessorarkitektur og ytelsesforbedring.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1020"]
    },
    {
        "id": "IN2090",
        "title": "Databaser og datamodellering",
        "title_english": "Databases and Data Modelling",
        "description": "Emnet gir en innf\u00f8ring i relasjonsdatabaser, SQL, ER-modellering, normalisering og transaksjonsbehandling. Studentene l\u00e6rer \u00e5 designe og implementere databaser.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN2120",
        "title": "Informasjonssikkerhet",
        "title_english": "Information Security",
        "description": "Emnet gir en oversikt over sentrale temaer i informasjonssikkerhet, inkludert kryptografi, autentisering, tilgangskontroll, nettverkssikkerhet og sikkerhetspolicyer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1020"]
    },
    {
        "id": "IN2140",
        "title": "Introduksjon til operativsystemer og datakommunikasjon",
        "title_english": "Introduction to Operating Systems and Data Communication",
        "description": "Emnet gir en grunnleggende innf\u00f8ring i operativsystemer og datakommunikasjon. Operativsystemer: prosesser, tr\u00e5der, synkronisering, minne- og filsystemer. Datakommunikasjon: protokollstabler, TCP/IP, ruting.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010", "IN1020"]
    },
    {
        "id": "IN2150",
        "title": "Introduksjon til cybersikkerhet for ledere",
        "title_english": "Introduction to Cybersecurity for Managers",
        "description": "Emnet gir en innf\u00f8ring i cybersikkerhet fra et lederperspektiv, med fokus p\u00e5 risikovurdering, sikkerhetsstyring, og organisatoriske aspekter av informasjonssikkerhet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Hjemmeeksamen",
        "teaching_form": "2 timer forelesning og 2 timer seminar per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "IN2310",
        "title": "Digital Forensics",
        "title_english": "Digital Forensics",
        "description": "Emnet gir en innf\u00f8ring i digital etterforskning og bevisinnhenting, inkludert filsystemer, minneanalyse, nettverksetterforskning og mobile enheter.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "English",
        "exam_form": "4 timers skriftlig eksamen + obligatorisk lab",
        "teaching_form": "2 timer forelesning og 2 timer lab per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2140"]
    },
    {
        "id": "IN3020",
        "title": "Databaser og datalagring",
        "title_english": "Databases and Data Storage",
        "description": "Emnet gir en videref\u00f8ring i databaseteknologi med fokus p\u00e5 avanserte emner som sp\u00f8rreoptimalisering, transaksjonsbehandling, NoSQL-databaser, og distribuerte systemer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig digital eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2090"]
    },
    {
        "id": "IN3030",
        "title": "Effektiv parallellprogrammering",
        "title_english": "Efficient Parallel Programming",
        "description": "Emnet gir en innf\u00f8ring i parallellprogrammering med fokus p\u00e5 ytelse. Emnet dekker tr\u00e5dprogrammering, synkronisering, parallelle algoritmer og bruk av GPU for beregninger.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010", "IN2140"]
    },
    {
        "id": "IN3040",
        "title": "Introduksjon til kunstig intelligens",
        "title_english": "Introduction to Artificial Intelligence",
        "description": "Emnet gir en innf\u00f8ring i kunstig intelligens med fokus p\u00e5 s\u00f8kealgoritmer, maskinl\u00e6ring, naturlig spr\u00e5kbehandling og robotikk.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN3050",
        "title": "Introduksjon til kunstig intelligens og maskinl\u00e6ring",
        "title_english": "Introduction to Artificial Intelligence and Machine Learning",
        "description": "Emnet gir en innf\u00f8ring i sentrale temaer innenfor kunstig intelligens og maskinl\u00e6ring. S\u00f8k, optimalisering, supervised og unsupervised l\u00e6ring, evolusjon\u00e6re algoritmer.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN3060",
        "title": "Spr\u00e5kteknologi",
        "title_english": "Language Technology",
        "description": "Emnet gir en innf\u00f8ring i automatisk behandling av naturlig spr\u00e5k (NLP), inkludert maskinoversettelse, sentimentanalyse, informasjonsekstraksjon, og spr\u00e5kmodeller.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Hjemmeeksamen",
        "teaching_form": "2 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2010"]
    },
    {
        "id": "IN3070",
        "title": "Logikk",
        "title_english": "Logic",
        "description": "Emnet gir en grundig innf\u00f8ring i matematisk logikk: fullstendighetssetningen, kompakthet, L\u00f6wenheim-Skolem, ufullstendighetssetningene, ber\u00e8knbarhet og uavgj\u00f8rbarhet.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers avsluttende skriftlig eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["IN1150"]
    },
    {
        "id": "IN3110",
        "title": "Probleml\u00f8sning med h\u00f8yniv\u00e5-programmering",
        "title_english": "Problem Solving with High-Level Programming",
        "description": "Emnet gir en innf\u00f8ring i h\u00f8yniv\u00e5-programmering med Python og relaterte verkt\u00f8y for vitenskapelig programmering, inklusive C-integrasjon, parallellisering og avansert databehandling.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Prosjektbasert",
        "teaching_form": "2 timer forelesning og 2 timer lab per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1000"]
    },
    {
        "id": "MAT1100",
        "title": "Kalkulus",
        "title_english": "Calculus",
        "description": "Emnet gir en innf\u00f8ring i analyse av funksjoner av \u00e9n variabel, inkludert grenser, kontinuitet, derivasjon, integrasjon og Taylors formel.",
        "instructor": None,
        "credits": 10,
        "department": "Mathematics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": []
    },
    {
        "id": "MAT1110",
        "title": "Kalkulus og line\u00e6r algebra",
        "title_english": "Calculus and Linear Algebra",
        "description": "Emnet gir en innf\u00f8ring i flervariabelanalyse og line\u00e6r algebra: Vektorer, matriser, line\u00e6re likningssystemer, egenverdier, funksjoner av flere variable, partielle deriverte og dobbeltintegraler.",
        "instructor": None,
        "credits": 10,
        "department": "Mathematics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["MAT1100"]
    },
    {
        "id": "STK1100",
        "title": "Sannsynlighetsregning og statistisk modellering",
        "title_english": "Probability and Statistical Modelling",
        "description": "Emnet gir en innf\u00f8ring i sannsynlighetsteori og statistikk, inkludert sannsynlighetsfordelinger, forventning, varians, estimering og hypotesetesting.",
        "instructor": None,
        "credits": 10,
        "department": "Mathematics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "4 timers skriftlig eksamen",
        "teaching_form": "4 timer forelesning og 2 timer gruppeundervisning per uke",
        "weekly_hours": 6,
        "prerequisite_ids": ["MAT1100"]
    },
    {
        "id": "INEC1831",
        "title": "Strategi",
        "title_english": "Strategy",
        "description": "I dette emnet l\u00e6rer du om de mest sentrale teoretiske retningene innenfor strategifaget, og hvilke av disse hovedskolene som er mest hensiktsmessig \u00e5 benytte for \u00e5 l\u00f8se ulike konkrete strategiske problemstillinger i ulike typer virksomheter eller organisasjoner. Strategifaget bygger videre p\u00e5 \u00f8konomi, markedsf\u00f8ring og organisasjonsfagene, og integrerer disse i dette strategiemnet. Emnet vil ta utgangspunkt i konkrete og relevante problemstillinger og analysere disse ved gruppearbeid og diskusjoner. Mesteparten av l\u00e6ringen i dette emnet skjer derfor gjennom aktiv diskusjon som krever forberedelser og klasseromsdeltakelse av den enkelte.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring"],
        "language": "Norwegian",
        "exam_form": "Prosjektoppgave gjort i grupper av 2-4 studenter (50%). Individuell muntlig presentasjon etterfulgt av sp\u00f8rsm\u00e5l fra eksaminator og sensor (50%)",
        "teaching_form": "2 timer forelesning og 2 timer gruppe\u00f8velser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "INEC1821",
        "title": "Digital \u00f8konomi, organisering og ledelse",
        "title_english": "Digital Economy, Organization and Leadership",
        "description": "Digital \u00f8konomi, organisering og ledelse handler om \u00e5 forst\u00e5 hvordan moderne organisasjoner er bygget opp og fungerer, og hvordan ledere oppn\u00e5r resultater. Gjennom emnet f\u00e5r du grunnleggende innsikt i organisasjons- og ledelsesteori, nye digitale organisasjonsformer, og transformasjonsledelse. Det vil gis en innf\u00f8ring i digital \u00f8konomi, herunder digitalisering, digitale plattformer og \u00f8kosystemer. Emnet vil ogs\u00e5 ta for seg hvordan bedrifter bruker data for \u00e5 ta beslutninger.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Prosjektoppgave med muntlig presentasjon, gjort i grupper av 2-4 studenter (60%). Muntlig eksamen i gruppe med individuell vurdering (40%)",
        "teaching_form": "2 timer forelesning og 2 timer gruppe\u00f8velser per uke",
        "weekly_hours": 4,
        "prerequisite_ids": []
    },
    {
        "id": "INEC1810",
        "title": "Marknad, markedsf\u00f8ring og produktutvikling",
        "title_english": "Market, Marketing and Product Development",
        "description": "I dette emnet l\u00e6rer du hvordan kunder skapes og betjenes. Hva kunden \u00f8nsker, utforming av produkter og tjenester tilpasset dette, og kommunikasjon om det som tilbys til kunder og andre interessenter - samt hvordan forholde seg til kortsiktig og langsiktig l\u00f8nnsomhet i markeder. Spesiell oppmerksomhet er viet informasjons\u00f8konomi - hvordan kj\u00f8p og salg av informasjonsvarer - som data og programvare - skiller seg fra fysiske varer og tjenester, samt hvordan bedriften kan styre forholdet mellom produktutvikling og markedsf\u00f8ring ved \u00e5 tilpasse kundekrav og teknologiske muligheter i en dialog.",
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
        "title": "\u00c5 forst\u00e5 bruk f\u00f8r bruk",
        "title_english": "Understanding Use Before Use",
        "description": "Emnet gir en oversikt over hva interaksjonsdesignere b\u00f8r vite om bruk og brukskontekst for \u00e5 designe optimale og brukervennlige digitale artefakter og systemer og forst\u00e5 utfordringene ved \u00e5 designe for bruk. Det legges vekt p\u00e5 begreper og teorier, illustrert med eksempler fra hverdagsliv og forskning. Emnet skal trene studentenes forestillingevne og evne til \u00e5 tenke alternativt om menneskers relasjoner til digitale artefakter og systemer p\u00e5 kort og lang sikt.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Muntlig gruppeeksamen med individuell karakter",
        "teaching_form": "2 timer forelesning og 2 timer \u00f8vingsgrupper pr. uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN1060"]
    },
    {
        "id": "IN3230",
        "title": "Nettverk",
        "title_english": "Networks",
        "description": "Dette emnet gir en grunnleggende innf\u00f8ring i sentrale funksjoner i kommunikasjonssystemer, herunder adressering, ruting, flytkontroll, feilh\u00e5ndtering, p\u00e5litelighet og synkronisering. Det blir gitt eksempler p\u00e5 hvordan disse funksjonene anvendes i dagens kommunikasjonssystemer, og mer spesifikt hvordan disse anvendes innen ulike nettverksteknologier. Sentrale arkitekturer og protokoller gjennomg\u00e5s.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "En deleksamen som teller 30%, og en avsluttende eksamen som teller 70%. Den avsluttende eksamen er en 4 timers skriftlig digital eksamen eller muntlig",
        "teaching_form": "2 timer forelesning og 2 timer felles oppgavel\u00f8sning per uke",
        "weekly_hours": 4,
        "prerequisite_ids": ["IN2140"]
    },
    {
        "id": "IN3240",
        "title": "Testing av programvare",
        "title_english": "Software Testing",
        "description": "Emnet dekker fundamentale begreper innenfor testing av programvare og spesifikke omr\u00e5der som: testing gjennom livssyklusen til et programvaresystem, statiske teknikker for testing, testdesign teknikker, testledelse, verkt\u00f8yst\u00f8tte for testing, testing av brukeropplevelser, testing av tilgjengelighet, eksplorativ testing, automatisert testing, testdrevet utvikling.",
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
        "description": "I dette emnet vil studenten sammen med veileder utforske og rapportere om et tema innen interaksjonsdesign. Oppgaven som skal utf\u00f8res vil involvere design og utvikling av h\u00f8yoppg\u00e5ende designartefakter i samr\u00e5d med sluttbrukere hvor datainnsamling, utvikling og evaluering inng\u00e5r som en del av eksperimentet. Emnet egner seg for studenter som \u00f8nsker \u00e5 jobbe med enten etablerte n\u00e6ringslivscase eller p\u00e5g\u00e5ende forskningsprosjekter som utgangspunkt for en faglig fordypning innen interaksjonsdesign.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["fall"],
        "language": "Norwegian",
        "exam_form": "Vurdering av skriftlig oppgave (70%), samt muntlig presentasjon av oppgaven (30%)",
        "teaching_form": "Tre fellessamlinger \u00e1 to timer og individuell veiledning",
        "weekly_hours": None,
        "prerequisite_ids": ["IN2020", "IN1060", "IN1010"]
    },
    {
        "id": "IN3260",
        "title": "Prosjektoppgave i informatikk: datakommunikasjon",
        "title_english": "Project Assignment in Informatics: Data Communication",
        "description": "I dette emnet vil studenten sammen med veileder utforske og rapportere om et tema innen datakommunikasjon. Oppgaven som skal utf\u00f8res vil vanligvis ha en praktisk komponent der studenten skal programmere og evaluere et eksperiment eller en applikasjon. Emnet egner seg for studenter som kan tenke seg en dypere forst\u00e5else av en del av datakommunikasjonsfaget og/eller en forsknings- eller utviklingskarriere i datakommunikasjon.",
        "instructor": None,
        "credits": 10,
        "department": "Informatics",
        "level": "bachelor",
        "semester": ["spring", "fall"],
        "language": "Norwegian",
        "exam_form": "Vurdering av skriftlig oppgave (70%), samt muntlig presentasjon av oppgaven (30%)",
        "teaching_form": "Tre fellessamlinger \u00e1 to timer og individuell veiledning",
        "weekly_hours": None,
        "prerequisite_ids": ["IN1010"]
    },
    {
        "id": "IN3290",
        "title": "Digital teknologi og samfunn",
        "title_english": "Digital Technology and Society",
        "description": "Emnet utforsker samspillet mellom digital teknologi og samfunnet bredt forst\u00e5tt. Dette inkluderer forholdet mellom digital teknologi og mellommenneskelige relasjoner, politikk og demokrati, n\u00e6ringsliv og innovasjon, forskning og b\u00e6rekraft. Sentralt for emnet er antagelsen om at digital teknologi har en klar p\u00e5virkning p\u00e5 v\u00e5re samfunn, men at vi som individer, grupper og samfunn ogs\u00e5 uunng\u00e5elig p\u00e5virker hvilke teknologiske l\u00f8sninger som utvikles og velges.",
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
        "title": "Dyp l\u00e6ring for bildeanalyse",
        "title_english": "Deep Learning for Image Analysis",
        "description": "Dette emnet underviser i vanlige metoder innen dyp l\u00e6ring anvendt p\u00e5 bildedata, og dekker viktige algoritmer og konsepter i dyp l\u00e6ring for \u00e5 trene nevrale nettverk. Emnet fokuserer p\u00e5 veiledet l\u00e6ring og bildegjenkjenning, men vil ogs\u00e5 introdusere andre vanlige l\u00e6ringsregimer og bildeanalyseoppgaver, som bildesegmentering og objektgjenkjenning.",
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
        "exam_form": "Avsluttende digital eksamen p\u00e5 4 timer",
        "teaching_form": "2 timer forelesning og 2 timer \u00f8velser per uke",
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
        db.execute(prerequisite_table.delete())
        deleted_count = db.query(Course).delete()
        db.commit()
        print(f"Cleared {deleted_count} courses and all prerequisite relationships")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()


def seed_real_courses():
    """Seed database with real UiO course data"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Starting to seed courses...")

        # First pass: create all courses without prerequisites
        course_objects = {}
        for course_data in all_courses_data:
            existing = db.query(Course).filter(Course.id == course_data["id"]).first()
            if existing:
                print(f"  {course_data['id']} already exists, skipping")
                course_objects[course_data["id"]] = (existing, course_data.get('prerequisite_ids', []))
                continue

            prereq_ids = course_data.pop('prerequisite_ids', [])
            course = Course(**course_data)
            db.add(course)
            course_objects[course.id] = (course, prereq_ids)

        db.commit()
        print(f"Committed {len(course_objects)} courses")

        # Second pass: add prerequisites
        prereq_count = 0
        for course_id, (course, prereq_ids) in course_objects.items():
            for prereq_id in prereq_ids:
                prereq = db.query(Course).filter(Course.id == prereq_id).first()
                if prereq and prereq not in course.prerequisites:
                    course.prerequisites.append(prereq)
                    prereq_count += 1
                elif not prereq:
                    print(f"  Warning: prerequisite {prereq_id} not found for {course_id}")

        db.commit()

        total = db.query(Course).filter(Course.is_active == True).count()
        print(f"Done: {total} active courses, {prereq_count} prerequisite relationships")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def verify_courses():
    """Verify the seeded courses"""
    db = SessionLocal()
    try:
        total = db.query(Course).count()
        print(f"Total courses: {total}")

        courses_with_prereqs = db.query(Course).filter(
            Course.prerequisites.any()
        ).all()

        print(f"\nCourses with prerequisites ({len(courses_with_prereqs)}):")
        for course in courses_with_prereqs:
            prereq_ids = [p.id for p in course.prerequisites]
            print(f"  {course.id}: {course.title} -> {', '.join(prereq_ids)}")
    except Exception as e:
        print(f"Error verifying courses: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys as _sys

    command = _sys.argv[1] if len(_sys.argv) > 1 else "reset"
    commands = {
        "clear": clear_database,
        "seed": seed_real_courses,
        "verify": verify_courses,
        "reset": lambda: (clear_database(), seed_real_courses()),
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command '{command}'. Use: clear, seed, verify, or reset")
