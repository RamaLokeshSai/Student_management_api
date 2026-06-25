from sqlalchemy.orm import Session
import models
import schemas

# 1. READ: Get a single student by their unique ID
def get_student(db: Session, student_id: int):
    # db.query(models.Student) starts a query on the students table.
    # .filter(models.Student.id == student_id) acts like a SQL WHERE clause.
    # .first() returns the first result found, or None if no match is found.
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# 2. READ: Get a student by email (useful to verify uniqueness)
def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

# 3. READ: Get a list of students (with pagination)
# skip: How many records to skip (offset)
# limit: Maximum number of records to return
def get_students(db: Session, skip: int = 0, limit: int = 100):
    # .offset(skip) skips the first N rows.
    # .limit(limit) limits the result set size.
    # .all() fetches all matching rows from the database as a Python list.
    return db.query(models.Student).offset(skip).limit(limit).all()

# 4. CREATE: Add a new student
def create_student(db: Session, student: schemas.StudentCreate):
    # Convert Pydantic schema model (schemas.StudentCreate) to SQLAlchemy database model (models.Student)
    # student.dict() or student.model_dump() extracts the data as a dictionary.
    # ** unpacks the dictionary key-value pairs as arguments to the Student constructor.
    db_student = models.Student(
        name=student.name,
        email=student.email,
        age=student.age,
        grade=student.grade
    )
    # Add the new student object to the database session.
    db.add(db_student)
    # Save (commit) the transaction to the database.
    db.commit()
    # Refresh the db_student instance to retrieve the database-generated ID.
    db.refresh(db_student)
    return db_student

# 5. UPDATE: Update an existing student's details
def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate):
    # First, fetch the existing student from the database.
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    # Extract the update fields from the schema (excluding unset/None fields)
    update_data = student_update.model_dump(exclude_unset=True)
    
    # Loop through the fields and update the database model instance.
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    # Commit changes to database.
    db.commit()
    # Refresh to load updated properties.
    db.refresh(db_student)
    return db_student

# 6. DELETE: Remove a student from the database
def delete_student(db: Session, student_id: int):
    # Fetch the existing student.
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    # Mark the record for deletion in the session.
    db.delete(db_student)
    # Commit the transaction to apply the deletion to SQLite.
    db.commit()
    return db_student
