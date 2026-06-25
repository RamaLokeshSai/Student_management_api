from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import engine, get_db

# 1. Initialize Database Tables
# This command tells SQLAlchemy to create all tables defined in models.py (if they don't already exist).
# For a beginner project, doing this on startup is easy and ensures the SQLite database file
# 'students.db' is created automatically.
models.Base.metadata.create_all(bind=engine)

# 2. Create the FastAPI Application Instance
# This is the entrypoint to our web service.
app = FastAPI(
    title="Student Management API",
    description="A beginner-friendly REST API for managing student records using FastAPI, SQLite, and SQLAlchemy.",
    version="1.0.0"
)

# 3. ROOT ENDPOINT
# A simple welcome message at the base URL.
@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Student Management API! Visit /docs for the interactive Swagger UI."
    }

# 4. CREATE Endpoint: Add a new student
# - response_model=schemas.Student: This ensures the returned JSON matches our Student response schema.
# - status_code=status.HTTP_201_CREATED: Standard HTTP code for successful resource creation.
@app.post("/students", response_model=schemas.Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Check if a student with the email already exists. Email must be unique.
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(
            status_code=400, 
            detail=f"Email '{student.email}' is already registered."
        )
    # If email is unique, create the student.
    return crud.create_student(db=db, student=student)

# 5. READ ALL Endpoint: Retrieve a list of students
# - response_model=List[schemas.Student]: Tells FastAPI to expect a list of student records in return.
@app.get("/students", response_model=List[schemas.Student], tags=["Students"])
def view_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

# 6. READ BY ID Endpoint: Search for a single student by their ID
@app.get("/students/{student_id}", response_model=schemas.Student, tags=["Students"])
def search_student_by_id(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with ID {student_id} not found."
        )
    return db_student

# 7. UPDATE Endpoint: Modify an existing student's details
@app.put("/students/{student_id}", response_model=schemas.Student, tags=["Students"])
def update_student(student_id: int, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    # If the email is being updated, verify it doesn't conflict with another student's email.
    if student_update.email is not None:
        db_student_email = crud.get_student_by_email(db, email=student_update.email)
        if db_student_email and db_student_email.id != student_id:
            raise HTTPException(
                status_code=400,
                detail=f"Email '{student_update.email}' is already in use by another student."
            )

    updated_student = crud.update_student(db=db, student_id=student_id, student_update=student_update)
    if updated_student is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with ID {student_id} not found."
        )
    return updated_student

# 8. DELETE Endpoint: Remove a student record
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db=db, student_id=student_id)
    if deleted_student is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with ID {student_id} not found."
        )
    return {"detail": f"Student with ID {student_id} was successfully deleted."}

# 9. Direct Execution Block (for IDE Run buttons)
# This check checks if this file is run directly (e.g. `python main.py` or clicking "Run" in your IDE).
# If true, it starts the Uvicorn web server programmatically on port 8000.
if __name__ == "__main__":
    import uvicorn
    # Start the server: main is the name of the module/file, app is the FastAPI object inside it.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

