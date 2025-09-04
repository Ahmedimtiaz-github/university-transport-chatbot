import pandas as pd
import mysql.connector
from database_config import MYSQL_CONFIG

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def import_students_data():
    try:
        # Read Excel file
        df = pd.read_excel("Student Data.xlsx")
        
        # Connect to MySQL
        conn = connect_to_mysql()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert data into students table
        for _, row in df.iterrows():
            query = """
                INSERT INTO students (serial_number, name, semester)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    semester = VALUES(semester)
            """
            values = (row['Ser'], row['Student Name'], 'Spring 2024')  # Default semester
            cursor.execute(query, values)
        
        conn.commit()
        print("Student data imported successfully!")
        
    except Exception as e:
        print(f"Error importing student data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def import_drivers_data():
    try:
        # Read Excel file
        df = pd.read_excel("TPT Driver Detail.xlsx")
        
        # Connect to MySQL
        conn = connect_to_mysql()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert data into drivers table
        for _, row in df.iterrows():
            query = """
                INSERT INTO drivers (driver_name, contact_number)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    contact_number = VALUES(contact_number)
            """
            values = (row['Name'], str(row['Cell No']))
            cursor.execute(query, values)
        
        conn.commit()
        print("Driver data imported successfully!")
        
    except Exception as e:
        print(f"Error importing driver data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def import_routes_data():
    try:
        # Read Excel file
        df = pd.read_excel("Transport.xlsx")
        
        # Connect to MySQL
        conn = connect_to_mysql()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert data into routes table
        for _, row in df.iterrows():
            query = """
                INSERT INTO routes (route_number, route_shift, bus_number)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    route_shift = VALUES(route_shift),
                    bus_number = VALUES(bus_number)
            """
            values = (row['Routes'], row['\nRoute Shift'], row['Buses Number '])
            cursor.execute(query, values)
        
        conn.commit()
        print("Route data imported successfully!")
        
    except Exception as e:
        print(f"Error importing route data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def import_student_routes():
    try:
        # Read Excel file
        df = pd.read_excel("transportation-to-work-1.xlsx")
        
        # Connect to MySQL
        conn = connect_to_mysql()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Get student and route IDs for mapping
        cursor.execute("SELECT system_id, serial_number FROM students")
        student_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id, route_number FROM routes")
        route_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Insert data into student_routes table
        for _, row in df.iterrows():
            query = """
                INSERT INTO student_routes (student_id, route_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    route_id = VALUES(route_id)
            """
            student_id = student_map.get(row['Student ID'], None)
            route_id = route_map.get(row['Route'], None)
            
            if student_id and route_id:
                values = (student_id, route_id)
                cursor.execute(query, values)
        
        conn.commit()
        print("Student-route mapping imported successfully!")
        
    except Exception as e:
        print(f"Error importing student-route mapping: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Starting data import...")
    import_students_data()
    import_drivers_data()
    import_routes_data()
    import_student_routes()
    print("Data import complete!") 