from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from .models import CourseLevel, Semester

class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    title_english: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    credits: int = Field(..., ge=0, le=60)  # 0-60 credits
    department: str
    level: CourseLevel
    semester: List[Semester] = []
    language: str = "Norwegian"
    exam_form: Optional[str] = None
    teaching_form: Optional[str] = None
    weekly_hours: Optional[int] = Field(None, ge=0, le=40)

class CourseCreate(CourseBase):
    id: str = Field(..., pattern="^[A-Z]{2,4}[0-9]{4}$")  # Validates format like "IN1000"
    prerequisite_ids: List[str] = []
    
    @validator('id')
    def validate_course_id(cls, v):
        if not v or len(v) < 5:
            raise ValueError('Course ID must be at least 5 characters')
        return v.upper()

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    title_english: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    credits: Optional[int] = None
    department: Optional[str] = None
    level: Optional[CourseLevel] = None
    semester: Optional[List[Semester]] = None # Should be enum Semester not String
    language: Optional[str] = None
    prerequisite_ids: Optional[List[str]] = None
    is_active: Optional[bool] = None
    exam_form: Optional[str] = None
    teaching_form: Optional[str] = None
    weekly_hours: Optional[int] = None

class Course(CourseBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    prerequisites: List['Course'] = []  # Nested courses
    
    class Config:
        from_attributes = True