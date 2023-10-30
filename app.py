import pymysql
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from db import mysql
from time import sleep
app = Flask(__name__)
app.secret_key = "ez2eaksjd8o002uejkdasjd982ueashdjashd9o2ue29"


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/courses")
def list_courses():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Course;")
    rows = cursor.fetchall()
    for row in rows:
        # get date start and end and convert to human readable format
        row["StartDate"] = row["StartDate"].strftime("%d/%m/%Y")
        row["EndDate"] = row["EndDate"].strftime("%d/%m/%Y")
    return render_template("courses.html", rows=rows)


@app.route("/add_course", methods=["POST"])
def add_course():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    courseID, courseName, courseDescription, startDate, endDate, instructorID = (
        request.form["courseID"],
        request.form["courseName"],
        request.form["description"],
        request.form["startDate"],
        request.form["endDate"],
        request.form["instructorID"],
    )

    # check if course already exists
    cursor.execute(
        f"SELECT CourseID FROM Course WHERE CourseID = {courseID};",
    )

    if rows := cursor.fetchall():
        flash(f"Course with ID {courseID} already exists as {courseName}", "error")
        return redirect("/")

    cursor.execute(
        f"INSERT INTO Course (CourseID, CourseName, CourseDescription, StartDate, EndDate, InstructorID) VALUES ({courseID}, '{courseName}', '{courseDescription}', '{startDate}', '{endDate}', {instructorID});",

    )
    conn.commit()

    flash(f"Course {courseName} Added")
    return redirect("/")

@app.route("/validate_course_id", methods=["GET"])
def validate_course_id():
    courseID = request.args.get("courseID")

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if the courseID already exists
    cursor.execute(f"SELECT CourseID FROM Course WHERE CourseID = {courseID};")
    valid = not cursor.fetchone()
    return jsonify({"valid": valid})

@app.route("/search_course", methods=["POST"])
def search_course():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    search_query = request.form["search-query"]
    cursor.execute(
        f"SELECT * FROM Course WHERE CourseID LIKE '%{search_query}%' OR CourseName LIKE '%{search_query}%';")

    if rows := cursor.fetchall():
        for row in rows:
            # get date start and end and convert to human readable format
            row["StartDate"] = row["StartDate"].strftime("%d/%m/%Y")
            row["EndDate"] = row["EndDate"].strftime("%d/%m/%Y")
        return render_template("courses.html", rows=rows)
    else:
        flash(f"No Course Found Matching ID or Name as {search_query}", "error")
        return redirect("/")


@app.route("/delete_course/<int:courseID>", methods=["GET"])
def delete_course(courseID):
    # Use courseID directly from the route parameter
    print(courseID)

    # delete from database, check if exists
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        f"DELETE FROM Course WHERE CourseID = {courseID};",
    )
    conn.commit()

    # return back to the list of courses
    return redirect(url_for("list_courses"))


@app.route("/edit_course/<int:courseID>", methods=["GET", "POST"])
def edit_course(courseID):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # check if request method is get or post
    if request.method == "GET":
        cursor.execute(
            f"SELECT * FROM Course WHERE CourseID = {courseID};",
        )
        row = cursor.fetchone()
        # get date start and end and convert to human readable format
        row["StartDate"] = row["StartDate"].strftime(
            "%Y-%m-%d") if row["StartDate"] else ""
        row["EndDate"] = row["EndDate"].strftime(
            "%Y-%m-%d") if row["EndDate"] else ""
        return render_template("edit_course.html", row=row)

    else:
        courseID, courseName, courseDescription, startDate, endDate, instructorID = (
            request.form["courseID"],
            request.form["courseName"],
            request.form["description"],
            request.form["startDate"],
            request.form["endDate"],
            request.form["instructorID"],
        )

        # UPDATE THE RECORD
        cursor.execute(
           f"UPDATE Course SET CourseName = '{courseName}', CourseDescription = '{courseDescription}', StartDate = '{startDate}', EndDate = '{endDate}', InstructorID = {instructorID} WHERE CourseID = {courseID};",
        )

        conn.commit()
        flash(f"Course {courseName} Updated")
        return redirect(url_for("list_courses"))

if __name__ == "__main__":
    app.run(debug=True)
