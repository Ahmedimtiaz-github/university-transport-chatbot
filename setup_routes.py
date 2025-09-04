import mysql.connector
from database_config import MYSQL_CONFIG

def setup_routes():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    try:
        # First, let's add some routes if they don't exist
        routes = [
            ('Route-1', 'Morning', 'Bus-001'),
            ('Route-2', 'Evening', 'Bus-002'),
            ('Route-3', 'Morning', 'Bus-003')
        ]
        
        for route in routes:
            cursor.execute("""
                INSERT INTO routes (route_number, route_shift, bus_number) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE route_number=route_number
            """, route)
        
        # Get all students
        cursor.execute("SELECT system_id FROM students")
        students = cursor.fetchall()

        # Get the first route ID
        cursor.execute("SELECT id FROM routes LIMIT 1")
        route = cursor.fetchone()
        
        if route:
            route_id = route[0]
            
            # Map each student to the route
            for student in students:
                cursor.execute("""
                    INSERT INTO student_routes (student_id, route_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE route_id=VALUES(route_id)
                """, (student[0], route_id))

        conn.commit()
        print("Routes and mappings set up successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_routes() 