import models
from fastapi import FastAPI, Request, Depends
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import Student
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class StudentRequest(BaseModel):
    first_name: str
    last_name: str
    dob:str
    amount_due: int


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student)
    students = students.all()
    return students

@app.get("/getStudent/{student_id}")
def get_Student(student_id:int,db:Session=Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    return student

@app.put("/updateStudent/{student_id}")
def get_Student(student_id:int,student:StudentRequest,db:Session=Depends(get_db)):
    studentRecord = db.query(Student).filter(Student.id == student_id).first()
    studentRecord.first_name = student.first_name
    studentRecord.last_name = student.last_name
    studentRecord.amount_due = student.amount_due
    db.add(studentRecord)
    db.commit()
    db.refresh(studentRecord)
    return studentRecord

@app.delete("/deleteStudent/{student_id}")
def delete_Student(student_id:int,db:Session=Depends(get_db)):
    studentRecord = db.query(Student).filter(Student.id == student_id).first()
    db.delete(studentRecord)
    db.commit()
    return {"msg":"deleted"}


@app.post("/addStudent")
async def add_Student(student:StudentRequest ,db: Session = Depends(get_db)):
    print(student.first_name)
    stock = Student()
    stock.first_name = student.first_name
    stock.last_name = student.last_name
    stock.amount_due = student.amount_due
    db.add(stock)
    db.commit()
    return {
        "code":"hello",
        "student":student
    }