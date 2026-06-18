
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="School ERP", layout="wide")

conn = sqlite3.connect("school_erp.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
class_name TEXT,
roll_no TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS teachers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
subject TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
roll_no TEXT,
status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS results(
id INTEGER PRIMARY KEY AUTOINCREMENT,
roll_no TEXT,
marks INTEGER
)
""")
conn.commit()

st.title("🏫 School ERP Management System")

menu = st.sidebar.selectbox(
    "Select Module",
    ["Dashboard", "Students", "Teachers", "Attendance", "Results"]
)

if menu == "Dashboard":
    st.header("Dashboard")

    students = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    teachers = cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
    attendance = cur.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
    results = cur.execute("SELECT COUNT(*) FROM results").fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", students)
    c2.metric("Teachers", teachers)
    c3.metric("Attendance Records", attendance)
    c4.metric("Results", results)

elif menu == "Students":
    st.header("Student Management")

    with st.form("student_form"):
        name = st.text_input("Student Name")
        class_name = st.text_input("Class")
        roll_no = st.text_input("Roll Number")
        submit = st.form_submit_button("Add Student")

        if submit:
            cur.execute(
                "INSERT INTO students(name,class_name,roll_no) VALUES(?,?,?)",
                (name, class_name, roll_no)
            )
            conn.commit()
            st.success("Student Added")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

elif menu == "Teachers":
    st.header("Teacher Management")

    with st.form("teacher_form"):
        name = st.text_input("Teacher Name")
        subject = st.text_input("Subject")
        submit = st.form_submit_button("Add Teacher")

        if submit:
            cur.execute(
                "INSERT INTO teachers(name,subject) VALUES(?,?)",
                (name, subject)
            )
            conn.commit()
            st.success("Teacher Added")

    df = pd.read_sql_query("SELECT * FROM teachers", conn)
    st.dataframe(df, use_container_width=True)

elif menu == "Attendance":
    st.header("Attendance")

    with st.form("attendance_form"):
        roll_no = st.text_input("Roll Number")
        status = st.selectbox("Status", ["Present", "Absent"])
        submit = st.form_submit_button("Mark Attendance")

        if submit:
            cur.execute(
                "INSERT INTO attendance(roll_no,status) VALUES(?,?)",
                (roll_no, status)
            )
            conn.commit()
            st.success("Attendance Saved")

    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    st.dataframe(df, use_container_width=True)

elif menu == "Results":
    st.header("Result Management")

    with st.form("result_form"):
        roll_no = st.text_input("Roll Number")
        marks = st.number_input("Marks", 0, 100, 0)
        submit = st.form_submit_button("Save Result")

        if submit:
            cur.execute(
                "INSERT INTO results(roll_no,marks) VALUES(?,?)",
                (roll_no, marks)
            )
            conn.commit()
            st.success("Result Saved")

    df = pd.read_sql_query("SELECT * FROM results", conn)

    if not df.empty:
        df["Grade"] = df["marks"].apply(
            lambda m: "A" if m >= 90 else
                      "B" if m >= 75 else
                      "C" if m >= 50 else
                      "Fail"
        )

    st.dataframe(df, use_container_width=True)
