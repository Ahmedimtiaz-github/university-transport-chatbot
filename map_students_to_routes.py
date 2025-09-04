import mysql.connector
from database_config import MYSQL_CONFIG

def map_students_to_routes():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    try:
        # First get all students
        cursor.execute("SELECT system_id FROM students")
        students = cursor.fetchall()

        # Get all routes
        cursor.execute("SELECT id FROM routes")
        routes = cursor.fetchall()

        if not students or not routes:
            print("No students or routes found in the database")
            return

        # For this example, we'll assign the first route to all students
        # You should modify this logic based on your actual requirements
        route_id = routes[0][0]

        # Insert mappings
        for student in students:
            student_id = student[0]
            cursor.execute("""
                INSERT INTO student_routes (student_id, route_id)
                VALUES (%s, %s)
            """, (student_id, route_id))

        conn.commit()
        print("Successfully mapped students to routes!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    map_students_to_routes() 