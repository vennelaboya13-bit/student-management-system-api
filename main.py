
from datetime import date, datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models, schemas
from app.TeacherSalary import router as salary_router


# Create database tables
Base.metadata.create_all(bind=engine)


# FastAPI Application
app = FastAPI(
    title="Student Management System API",
    description="Student and Teacher Management REST API",
    version="1.0.0"
)

# Register Teacher Salary API
app.include_router(salary_router)


# =========================
# HOME AND HEALTH
# =========================

@app.get("/")
def home():
    return {
        "message": "Student Management System API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "OK"}


# =========================
# STUDENT REGISTRATION
# =========================

@app.post("/students", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(models.Student).filter(
        models.Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student email already registered"
        )

    new_student = models.Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# =========================
# STUDENT CHECK-IN
# =========================

@app.post("/students/{student_id}/check-in")
def student_check_in(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    today = date.today()

    attendance = db.query(models.StudentAttendance).filter(
        models.StudentAttendance.student_id == student_id,
        models.StudentAttendance.attendance_date == today
    ).first()

    if attendance:
        raise HTTPException(
            status_code=400,
            detail="Attendance already exists for today"
        )

    attendance = models.StudentAttendance(
        student_id=student_id,
        attendance_date=today,
        check_in=datetime.now().time().replace(microsecond=0),
        check_out=None,
        status="Present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Student check-in successful",
        "student_id": student_id,
        "attendance_date": attendance.attendance_date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status
    }


# =========================
# STUDENT CHECK-OUT
# =========================

@app.post("/students/{student_id}/check-out")
def student_check_out(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    today = date.today()

    attendance = db.query(models.StudentAttendance).filter(
        models.StudentAttendance.student_id == student_id,
        models.StudentAttendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Student check-in record not found for today"
        )

    if attendance.check_out is not None:
        raise HTTPException(
            status_code=400,
            detail="Student has already checked out today"
        )

    attendance.check_out = datetime.now().time().replace(
        microsecond=0
    )

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Student check-out successful",
        "student_id": student_id,
        "attendance_date": attendance.attendance_date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status
    }


# =========================
# GET STUDENT ATTENDANCE
# =========================

@app.get(
    "/student-attendance",
    response_model=list[schemas.StudentAttendanceResponse]
)
def get_student_attendance(
    db: Session = Depends(get_db)
):
    return db.query(models.StudentAttendance).all()


# =========================
# TEACHER REGISTRATION
# =========================

@app.post("/teachers", response_model=schemas.TeacherResponse)
def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Session = Depends(get_db)
):
    existing_teacher = db.query(models.Teacher).filter(
        models.Teacher.email == teacher.email
    ).first()

    if existing_teacher:
        raise HTTPException(
            status_code=400,
            detail="Teacher email already registered"
        )

    new_teacher = models.Teacher(
        name=teacher.name,
        email=teacher.email,
        phone=teacher.phone,
        subject=teacher.subject,
        salary=teacher.salary
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher


@app.get("/teachers", response_model=list[schemas.TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()


# =========================
# TEACHER CHECK-IN
# =========================

@app.post("/teachers/{teacher_id}/check-in")
def teacher_check_in(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    teacher = db.query(models.Teacher).filter(
        models.Teacher.id == teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    today = date.today()

    attendance = db.query(models.TeacherAttendance).filter(
        models.TeacherAttendance.teacher_id == teacher_id,
        models.TeacherAttendance.attendance_date == today
    ).first()

    if attendance:
        raise HTTPException(
            status_code=400,
            detail="Teacher attendance already exists for today"
        )

    attendance = models.TeacherAttendance(
        teacher_id=teacher_id,
        attendance_date=today,
        check_in=datetime.now().time().replace(microsecond=0),
        check_out=None,
        status="Present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Teacher check-in successful",
        "teacher_id": teacher_id,
        "attendance_date": attendance.attendance_date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status
    }


# =========================
# TEACHER CHECK-OUT
# =========================

@app.post("/teachers/{teacher_id}/check-out")
def teacher_check_out(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    teacher = db.query(models.Teacher).filter(
        models.Teacher.id == teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    today = date.today()

    attendance = db.query(models.TeacherAttendance).filter(
        models.TeacherAttendance.teacher_id == teacher_id,
        models.TeacherAttendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Teacher check-in record not found for today"
        )

    if attendance.check_out is not None:
        raise HTTPException(
            status_code=400,
            detail="Teacher has already checked out today"
        )

    attendance.check_out = datetime.now().time().replace(
        microsecond=0
    )

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Teacher check-out successful",
        "teacher_id": teacher_id,
        "attendance_date": attendance.attendance_date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status
    }


# =========================
# GET TEACHER ATTENDANCE
# =========================

@app.get(
    "/teacher-attendance",
    response_model=list[schemas.TeacherAttendanceResponse]
)
def get_teacher_attendance(
    db: Session = Depends(get_db)
):
    return db.query(models.TeacherAttendance).all()

