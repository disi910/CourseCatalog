
from sqlalchemy import Column, String, Integer, Text, ARRAY, Enum, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database import Base

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
