import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)



import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)



@app.route('/')
def index():
  
    return render_template('index.html')

#create a route to view individual student profile page along with the clubs they are in. sample id=903543188415905793
@app.route('/students/<id>')
def student(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s", (id,))
        res = cur.fetchall()
        conn.commit()
        student=list(res[0])
        print(student)

        cur.execute("SELECT * FROM clubs WHERE id IN (SELECT club_id FROM favorites WHERE student_id = %s)", (id,))
        clubs_in_student = cur.fetchall()
        conn.commit()
        clubs_in_student=[list(item) for item in clubs_in_student]  
        print(clubs_in_student)
    return render_template('student_profile.html', student=student, clubs_in_student=clubs_in_student)

# create a new route to return combined JSON for a student and their clubs
@app.route('/api/students/<id>')
def student_api(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cur.fetchone()
        conn.commit()

        cur.execute("SELECT clubs.* FROM clubs JOIN favorites ON clubs.id = favorites.club_id WHERE favorites.student_id = %s", (id,))
        clubs = cur.fetchall()
        conn.commit()

    student_dict = {
        "id": student[0],
        "name": student[1],
        "details": student[2],
        "image": student[3]
    }

    clubs_list = []
    for club in clubs:
        club_dict = {
            "id": club[0],
            "name": club[1],
            "description": club[2],
            "image": club[3]
        }
        clubs_list.append(club_dict)

    combined_dict = {
        "student": student_dict,
        "clubs": clubs_list
    }
    print(combined_dict)
    return combined_dict

       
    
#create a route to view individual club page along with the students in the club. sample id=903543188415905793
@app.route('/clubs/<id>')
def club(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM clubs WHERE id = %s", (id,))
        club = cur.fetchall()
        conn.commit()
        club=list(club[0])
        print(club)

        cur.execute("SELECT * FROM students WHERE id IN (SELECT student_id FROM favorites WHERE club_id = %s)", (id,))
        students_in_club = cur.fetchall()
        conn.commit()
        students_in_club=[list(item) for item in students_in_club]


    return render_template('club_profile.html', club=club, students_in_club=students_in_club)
# create a new route to return combined JSON for a club and its students
@app.route('/api/clubs/<id>')
def club_api(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM clubs WHERE id = %s", (id,))
        club = cur.fetchone()
        conn.commit()

        cur.execute("SELECT students.* FROM students JOIN favorites ON students.id = favorites.student_id WHERE favorites.club_id = %s", (id,))
        students = cur.fetchall()
        conn.commit()

    club_dict = {
        "id": club[0],
        "name": club[1],
        "description": club[2],
        "image": club[3]
    }

    students_list = []
    for student in students:
        student_dict = {
            "id": student[0],
            "name": student[1],
            "details": student[2],
            "image": student[3]
        }
        students_list.append(student_dict)

    combined_dict = {
        "club": club_dict,
        "students": students_list
    }
    print(combined_dict)
    return combined_dict

#create a route to view all students with their id, name, and email
@app.route('/students')
def students():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        res = cur.fetchall()
        conn.commit()
        students=[list(item) for item in res]
        print(res)
        return render_template('all_students.html', students=res)

#create a route to view all clubs with their id, name, and description
@app.route('/clubs')
def clubs():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM clubs")
        res = cur.fetchall()
        conn.commit()
        clubs=[list(item) for item in res]
        print(res)
        return render_template('all_clubs.html', clubs=clubs)
        




if __name__ == "__main__":
  app.run()
