
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TeacherSalary as TeacherSalaryModel, Teacher

router = APIRouter(
    prefix="/teacher-salaries",
    tags=["Teacher Salaries"]
)


class TeacherSalaryCreate(BaseModel):
    teacher_id: int
    month: str
    basic_salary: float
    deductions: float = 0


@router.post("/")
def add_teacher_salary(
    salary: TeacherSalaryCreate,
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == salary.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    existing_salary = db.query(TeacherSalaryModel).filter(
        TeacherSalaryModel.teacher_id == salary.teacher_id,
        TeacherSalaryModel.month == salary.month
    ).first()

    if existing_salary:
        raise HTTPException(
            status_code=400,
            detail="Salary already exists for this month"
        )

    if salary.basic_salary < 0 or salary.deductions < 0:
        raise HTTPException(
            status_code=400,
            detail="Salary and deductions cannot be negative"
        )

    if salary.deductions > salary.basic_salary:
        raise HTTPException(
            status_code=400,
            detail="Deductions cannot exceed basic salary"
        )

    record = TeacherSalaryModel(
        teacher_id=salary.teacher_id,
        month=salary.month,
        basic_salary=salary.basic_salary,
        deductions=salary.deductions,
        net_salary=salary.basic_salary - salary.deductions,
        status="Calculated"
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "teacher_id": record.teacher_id,
        "month": record.month,
        "basic_salary": record.basic_salary,
        "deductions": record.deductions,
        "net_salary": record.net_salary,
        "status": "Salary saved successfully"
    }


@router.get("/")
def get_teacher_salaries(db: Session = Depends(get_db)):
    records = db.query(TeacherSalaryModel).all()

    return [
        {
            "id": record.id,
            "teacher_id": record.teacher_id,
            "month": record.month,
            "basic_salary": record.basic_salary,
            "deductions": record.deductions,
            "net_salary": record.net_salary,
            "status": record.status
        }
        for record in records
    ]


@router.get("/{teacher_id}")
def get_teacher_salary_by_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    records = db.query(TeacherSalaryModel).filter(
        TeacherSalaryModel.teacher_id == teacher_id
    ).all()

    return [
        {
            "id": record.id,
            "teacher_id": record.teacher_id,
            "month": record.month,
            "basic_salary": record.basic_salary,
            "deductions": record.deductions,
            "net_salary": record.net_salary,
            "status": record.status
        }
        for record in records
    ]
