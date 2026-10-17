
from sqlalchemy import (
    Column, Integer, String, Date, Time,
    DateTime, ForeignKey, Float
)
from sqlalchemy.sql import func
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    class_name = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    subject = Column(String(100))
    salary = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())


class StudentAttendance(Base):
    __tablename__ = "student_attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer, ForeignKey("students.id"), nullable=False
    )
    attendance_date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    status = Column(String(20), nullable=False)


class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(
        Integer, ForeignKey("teachers.id"), nullable=False
    )
    attendance_date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    status = Column(
        String(20), nullable=False, default="Present"
    )


class TeacherSalary(Base):
    __tablename__ = "teacher_salaries"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(
        Integer, ForeignKey("teachers.id"), nullable=False
    )
    month = Column(String(7), nullable=False)
    basic_salary = Column(Float, nullable=False)
    deductions = Column(Float, nullable=False, default=0.0)
    net_salary = Column(Float, nullable=False)
    status = Column(
        String(20), nullable=False, default="Calculated"
    )
