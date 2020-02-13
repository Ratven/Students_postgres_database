import psycopg2

conn = psycopg2.connect(dbname="students_db", user="user2", password="user2")
cur = conn.cursor()


def create_db():  # создает таблицы
    cur.execute("""CREATE TABLE IF NOT EXISTS student(
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    gpa numeric(10,2),
    birth timestamp with time zone);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS course(
    id integer NOT NULL,
    name character varying(100) NOT NULL);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS student_course(
    id serial,
    student integer REFERENCES student(id),
    course integer REFERENCES course(id));
    """)
    conn.commit()


def get_students(course_id):  # возвращает студентов определенного курса
    cur.execute("SELECT student.name, student.gpa FROM student_course "
                "JOIN student on student_course.student = student.id WHERE student_course.course = (%s)", (course_id))
    return cur.fetchall()


def add_students(course_id, students):  # создает студентов и записывает их на курc
    for stud in students:
        add_student(stud)
        cur.execute("INSERT INTO student_course (student, course) values (%s, %s)", (stud['id'], course_id))
    conn.commit()


def add_student(student):  # просто создает студента
    cur.execute("INSERT INTO student VALUES (%s, %s, %s, %s)",
                (student['id'], student['name'], student['gpa'], student['birth']))


def get_student(student_id):
    cur.execute(f"SELECT name, gpa, birth FROM student WHERE id={student_id}")
    return cur.fetchall()


if __name__ == '__main__':
    stud1 = {
        'id': 26,
        'name': 'Alexeev',
        'gpa': 4.2,
        'birth': '1990-12-11'
    }

    stud2 = {
        'id': 27,
        'name': 'Smirnov',
        'gpa': 4.4,
        'birth': '1990-03-02'
    }

    course1 = {
        'id': 1,
        'name': 'Python'
    }

    course2 = {
        'id': 18,
        'name': 'Java'
    }

    create_db()
    stud_list = [stud1, stud2]
    # cur.execute("INSERT INTO course VALUES (%s, %s)", (course1['id'], course1['name']))
    add_students(1, stud_list)
    conn.commit()
    print('Success')
