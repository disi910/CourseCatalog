
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Ififag API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


courses = ["IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010","IN1000", "IN1020", "IN1010"]

@app.get("/")
async def main_route():
    return "Welcome to my API!! :D"


@app.get("/courses")
def get_courses():
    # Fake data for now
    return [
        {"id": "IN1000", "name": "Introduksjon til objektorientert programmering"},
        {"id": "IN1020", "name": "Introduksjon til datateknologi"}
    ]


@app.get("/courses/{course_id}")
async def get_courseslist(course_id: str) -> str:
    if course_id < len(courses):
        return courses[course_id]
    else:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
