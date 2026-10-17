
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date, time


# Student Registration
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    class_name: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    class_name: Optional[str] = None

    class Config:
        from_attributes = True


# Student Attendance
class StudentAttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Literal["Present", "Absent"] = "Present"


class StudentAttendanceResponse(BaseModel):
    id: int
    student_id: int
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str

    class Config:
        from_attributes = True


# Teacher Registration
class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    salary: float = 0.0


class TeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    subject: Optional[str] = None
    salary: float

    class Config:
        from_attributes = True


# Teacher Attendance
class TeacherAttendanceCreate(BaseModel):
    teacher_id: int
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Literal["Present", "Absent"] = "Present"


class TeacherAttendanceResponse(BaseModel):
    id: int
    teacher_id: int
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str

    class Config:
        from_attributes = True
