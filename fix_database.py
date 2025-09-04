import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import re

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Warmsi@123',
            database='transport_management'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def fix_time_format(connection):
    cursor = connection.cursor()
    try:
        # First convert timedelta to proper time strings
        cursor.execute("SELECT id, start_time, end_time FROM routes")
        routes = cursor.fetchall()
        
        for route_id, start_time, end_time in routes:
            if isinstance(start_time, timedelta):
                hours = start_time.seconds // 3600
                minutes = (start_time.seconds % 3600) // 60
                start_time = f"{hours:02d}:{minutes:02d}:00"
            
            if isinstance(end_time, timedelta):
                hours = end_time.seconds // 3600
                minutes = (end_time.seconds % 3600) // 60
                end_time = f"{hours:02d}:{minutes:02d}:00"
            
            cursor.execute("""
                UPDATE routes 
                SET start_time = %s, end_time = %s 
                WHERE id = %s
            """, (start_time, end_time, route_id))
        
        # Now alter the column types
        cursor.execute("""
            ALTER TABLE routes 
            MODIFY COLUMN start_time TIME,
            MODIFY COLUMN end_time TIME
        """)
        
        connection.commit()
        print("Time formats fixed successfully")
    except Error as e:
        print(f"Error fixing time format: {e}")
    finally:
        cursor.close()

def assign_drivers_to_routes(connection):
    cursor = connection.cursor()
    try:
        # Read driver data from Excel
        driver_df = pd.read_excel('TPT Driver Detail.xlsx')
        
        # Read route data from Excel
        route_df = pd.read_excel('Transport.xlsx')
        
        # Create a mapping of route numbers to route IDs
        cursor.execute("SELECT id, route_number FROM routes")
        route_mapping = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Update drivers with route assignments
        for _, driver_row in driver_df.iterrows():
            driver_name = driver_row['Name'].strip()
            contact_number = str(driver_row['Cell No']).strip()
            
            # Find matching route for this driver
            cursor.execute("""
                UPDATE drivers 
                SET contact_number = %s
                WHERE name = %s
            """, (contact_number, driver_name))
        
        connection.commit()
        print("Drivers updated successfully")
        
        # Now assign routes based on Transport.xlsx
        route_df = pd.read_excel('Transport.xlsx')
        for _, route_row in route_df.iterrows():
            route_number = route_row['Routes'].strip()
            if route_number in route_mapping:
                route_id = route_mapping[route_number]
                # Find a driver without a route and assign this route
                cursor.execute("""
                    UPDATE drivers 
                    SET route_id = %s 
                    WHERE route_id IS NULL 
                    LIMIT 1
                """, (route_id,))
        
        connection.commit()
        print("Routes assigned to drivers successfully")
    except Error as e:
        print(f"Error assigning drivers to routes: {e}")
    finally:
        cursor.close()

def populate_student_routes(connection):
    cursor = connection.cursor()
    try:
        # Read student data from Excel
        student_df = pd.read_excel('Student Data.xlsx')
        route_df = pd.read_excel('Transport.xlsx')
        
        # Create mappings
        cursor.execute("SELECT id, system_id FROM students")
        student_mapping = {str(row[1]).strip().upper(): row[0] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id, route_number FROM routes")
        route_mapping = {str(row[1]).strip(): row[0] for row in cursor.fetchall()}
        
        # Clear existing student_routes
        cursor.execute("TRUNCATE TABLE student_routes")
        
        # Get all route IDs
        route_ids = list(route_mapping.values())
        if not route_ids:
            print("No routes found in database")
            return
        
        # Assign students to routes round-robin style
        for idx, student_row in student_df.iterrows():
            system_id = str(student_row['System Id']).strip().upper()
            if system_id in student_mapping:
                student_id = student_mapping[system_id]
                # Assign route round-robin style
                route_id = route_ids[idx % len(route_ids)]
                
                cursor.execute("""
                    INSERT INTO student_routes (student_id, route_id)
                    VALUES (%s, %s)
                """, (student_id, route_id))
        
        connection.commit()
        print("Student routes populated successfully")
    except Error as e:
        print(f"Error populating student routes: {e}")
    finally:
        cursor.close()

def main():
    connection = connect_to_database()
    if connection:
        try:
            print("Starting database fixes...")
            fix_time_format(connection)
            assign_drivers_to_routes(connection)
            populate_student_routes(connection)
            print("All fixes completed successfully")
        except Error as e:
            print(f"Error during database fixes: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    main() 