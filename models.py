from sqlalchemy import Column, Integer, String
from database import Base

# 1. Define the Student Model.
# This class inherits from the Base class we created in database.py.
# SQLAlchemy will map this class to a table in SQLite.
class Student(Base):
    # __tablename__ tells SQLAlchemy the exact name of the table in the database.
    __tablename__ = "students"

    # 2. Define Table Columns.
    # Each attribute represents a column in the database table.
    
    # id: An integer column that serves as the Primary Key. 
    # SQLAlchemy will automatically make this auto-incrementing in SQLite since it's an Integer Primary Key.
    id = Column(Integer, primary_key=True, index=True)

    # name: A string column storing the student's full name.
    name = Column(String, nullable=False)

    # email: A unique string column. No two students can have the same email address.
    # index=True creates an index in the database to speed up searches by email.
    email = Column(String, unique=True, index=True, nullable=False)

    # age: An integer column storing the student's age.
    age = Column(Integer, nullable=False)

    # grade: A string column representing the class or grade level (e.g., "10th Grade", "A+").
    grade = Column(String, nullable=False)
