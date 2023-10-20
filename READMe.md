# LMS CRUD App for DBMS ISE

1. Create a MySQL Database 'lms_group_06'
2. Write SQL query to create a table 'Courses'

This should be executed against the database before running the app

```sql
USE lms_group_06;

CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(255),
    CourseDescription VARCHAR(255),
    StartDate DATE,
    EndDate DATE,
    InstructorID INT
);
```


3. Install all dependencies using `pip install requirements.txt`

4. Run the flask app using `python .\run.py`

5. Browse the app via `http://127.0.0.1:5000`
