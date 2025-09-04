import pandas as pd
import mysql.connector
from database_config import MYSQL_CONFIG
import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def close_db_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()

def clean_value(val):
    if pd.isna(val):
        return None
    return str(val).strip()

def import_students():
    conn = None
    cursor = None
    try:
        # Read student data
        df = pd.read_excel('Student Data.xlsx')
        df.columns = ['Ser', 'Student Name', 'System Id']
        
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert students
        for _, row in df.iterrows():
            try:
                query = "INSERT INTO students (name, system_id) VALUES (%s, %s)"
                values = (clean_value(row['Student Name']), clean_value(row['System Id']))
                cursor.execute(query, values)
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate entry error
                    print(f"Skipping duplicate student: {row['System Id']}")
                    continue
                else:
                    raise err
        
        conn.commit()
        print(f"Imported {len(df)} students")
        
    except Exception as e:
        print(f"Error importing students: {str(e)}")
    finally:
        close_db_connection(conn, cursor)

def import_drivers():
    conn = None
    cursor = None
    try:
        # Read driver data
        df = pd.read_excel('TPT Driver Detail.xlsx')
        df.columns = ['Ser', 'Name', 'Department', 'Designation', 'Scale', 'Job Status', 'DOJ', 'Cell No']
        
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert drivers
        for _, row in df.iterrows():
            query = "INSERT INTO drivers (name, contact_number) VALUES (%s, %s)"
            values = (clean_value(row['Name']), clean_value(row['Cell No']))
            cursor.execute(query, values)
        
        conn.commit()
        print(f"Imported {len(df)} drivers")
        
    except Exception as e:
        print(f"Error importing drivers: {str(e)}")
    finally:
        close_db_connection(conn, cursor)

def import_routes():
    conn = None
    cursor = None
    try:
        # Read route data
        df = pd.read_excel('Transport.xlsx')
        df.columns = ['Routes', 'Route Shift', 'Buses Number']
        
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Insert routes
        imported = 0
        for _, row in df.iterrows():
            try:
                query = "INSERT INTO routes (route_number, route_shift, bus_number) VALUES (%s, %s, %s)"
                values = (clean_value(row['Routes']), clean_value(row['Route Shift']), clean_value(row['Buses Number']))
                cursor.execute(query, values)
                imported += 1
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate entry error
                    print(f"Skipping duplicate route: {row['Routes']}")
                    continue
                else:
                    raise err
        
        conn.commit()
        print(f"Imported {imported} routes")
        
    except Exception as e:
        print(f"Error importing routes: {str(e)}")
    finally:
        close_db_connection(conn, cursor)

def main():
    print("Starting data import...")
    import_students()
    import_drivers()
    import_routes()
    print("Data import completed!")

if __name__ == "__main__":
    main() 