from flask import Flask, render_template, request, redirect, url_for,session,flash, abort
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
DB = "database.sqlite3"

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    students = cur.execute("SELECT * FROM student").fetchall()
    conn.close()
    return render_template("index.html", students=students)



@app.route("/student/create", methods = ["GET","POST"])
def create_student():
	if request.method == "GET":
		return render_template("create_student.html")

	elif request.method == "POST":
		roll = request.form.get("roll")
		fname = request.form.get("f_name")
		lname = request.form.get("l_name")
		courses = request.form.getlist("courses")

		conn = sqlite3.connect(DB)
		cur = conn.cursor()
		existing = cur.execute("select * from student where roll_number=?",(roll,)).fetchone()
		if existing:
			conn.close()
			return render_template("error.html", message="Roll number already exists")

		cur.execute("insert into student (roll_number, first_name, last_name) values (?,?,?)",(roll,fname,lname))
		student_id = cur.lastrowid

		course_map = {
		    "course_1": 1,
		    "course_2": 2,
		    "course_3": 3,
		    "course_4": 4
		}

		courses = request.form.getlist("courses")

		for c in courses:
		    course_id = course_map.get(c)
		    cur.execute(
		        "INSERT INTO enrollments (estudent_id, ecourse_id) VALUES (?, ?)",
		        (student_id, course_id)
		    )

		conn.commit()
		conn.close()
		return redirect("/")


@app.route("/student/<int:id>/update", methods = ["GET","POST"])
def update_student(id):
	if request.method == "GET":
		conn = sqlite3.connect(DB)
	    cur = conn.cursor()

	    student = cur.execute(
	        "SELECT * FROM student WHERE student_id=?",
	        (id,)
	    ).fetchone()

	    enrolled = cur.execute(
	        "SELECT ecourse_id FROM enrollments WHERE estudent_id=?",
	        (id,)
	    ).fetchall()

	    enrolled_ids = [e[0] for e in enrolled]

	    conn.close()

	    return render_template(
	        "update_student.html",
	        id=id,
	        student=student,
	        enrolled_ids=enrolled_ids
	    )

	elif request.method == "POST":
		fname = request.form.get("f_name")
		lname = request.form.get("l_name")
		courses = request.form.getlist("courses")
		conn = sqlite3.connect(DB)
		cur = conn.cursor()
		cur.execute("UPDATE student SET first_name=?, last_name=? WHERE student_id=?",(fname, lname, id))
		cur.execute("DELETE FROM enrollments WHERE estudent_id=?",(id,))
		course_map = {"course_1": 1,"course_2": 2,"course_3": 3,"course_4": 4}
		for c in courses:
			course_id = course_map.get(c)
			cur.execute("INSERT INTO enrollments (estudent_id, ecourse_id) VALUES (?, ?)",(id, course_id))
		conn.commit()
		conn.close()
		return redirect("/")

	
@app.route("/student/<int:id>/delete")
def delete_std(id):
	conn = sqlite3.connect(DB)
	cur = conn.cursor()
	cur.execute("DELETE FROM enrollments WHERE estudent_id=?", (id,))
	cur.execute("DELETE FROM student WHERE student_id=?", (id,))
	conn.commit()
	conn.close()
	return redirect("/")


@app.route("/student/<int:id>")
def view_student(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Get student details
    student = cur.execute(
        "SELECT * FROM student WHERE student_id=?",
        (id,)
    ).fetchone()

    enrollments = cur.execute("""
        SELECT course.course_code, course.course_name, course.course_description
        FROM enrollments
        JOIN course ON enrollments.ecourse_id = course.course_id
        WHERE enrollments.estudent_id=?
    """, (id,)).fetchall()

    conn.close()

    return render_template(
        "view_student.html",
        student=student,
        enrollments=enrollments
    )

if __name__ == "__main__":
    app.run(debug=True)

