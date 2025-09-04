from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
from mysql.connector import pooling
from database_config import MYSQL_CONFIG
from rasa_sdk.events import SlotSet
import os

# Set environment variables to silence deprecation warnings
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'
os.environ['SQLALCHEMY_WARN_20'] = '0'

# Create a connection pool with improved configuration
dbconfig = {
    "host": MYSQL_CONFIG["host"],
    "user": MYSQL_CONFIG["user"],
    "password": MYSQL_CONFIG["password"],
    "database": MYSQL_CONFIG["database"],
    "pool_name": "mypool",
    "pool_size": 5,
    "autocommit": True,
    "buffered": True,
    "consume_results": True,
    "pool_reset_session": True
}

# Initialize connection pool
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
    print("Connection pool created successfully")
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

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

class ActionFetchRoute(Action):
    def name(self) -> Text:
        return "action_fetch_route"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            route_number = tracker.get_slot("route_number")
            
            if not route_number:
                dispatcher.utter_message(text="Please provide a route number to get route information.")
                return []
            
            query = """
                SELECT r.route_number, r.route_shift, r.bus_number, r.start_time, r.end_time,
                       d.name as driver_name, d.contact_number,
                       COUNT(DISTINCT sr.student_id) as student_count
                FROM routes r
                LEFT JOIN drivers d ON r.id = d.route_id
                LEFT JOIN student_routes sr ON r.id = sr.route_id
                WHERE r.route_number = %s
                GROUP BY r.id, r.route_number, r.route_shift, r.bus_number, r.start_time, r.end_time, d.name, d.contact_number
            """
            
            cursor.execute(query, (route_number,))
            result = cursor.fetchone()
            
            if result:
                response = f"Route {result['route_number']} Information:\n"
                response += f"Shift: {result['route_shift'] or 'Not specified'}\n"
                response += f"Bus Number: {result['bus_number'] or 'Not assigned'}\n"
                response += f"Timing: {result['start_time'] or 'Not set'} to {result['end_time'] or 'Not set'}\n"
                response += f"Total Students: {result['student_count']}\n"
                if result['driver_name']:
                    response += f"Driver: {result['driver_name']} ({result['contact_number']})"
                else:
                    response += "Driver: Not assigned"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find information for route {route_number}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching route information: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchDriverInfo(Action):
    def name(self) -> Text:
        return "action_fetch_driver_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            route_number = tracker.get_slot("route_number")
            
            if not route_number:
                dispatcher.utter_message(text="Please provide a route number to get driver information.")
                return []
            
            query = """
                SELECT d.name, d.contact_number, r.route_number, r.bus_number
                FROM routes r
                LEFT JOIN drivers d ON r.id = d.route_id
                WHERE r.route_number = %s
            """
            
            cursor.execute(query, (route_number,))
            result = cursor.fetchone()
            
            if result and result['name']:
                response = f"Driver Information for Route {result['route_number']}:\n"
                response += f"Name: {result['name']}\n"
                response += f"Contact: {result['contact_number']}\n"
                response += f"Bus Number: {result['bus_number']}"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find driver information for route {route_number}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching driver information: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchRouteStudents(Action):
    def name(self) -> Text:
        return "action_fetch_route_students"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            route_number = tracker.get_slot("route_number")
            
            query = """
                SELECT s.name, s.system_id
                FROM students s
                JOIN student_routes sr ON s.id = sr.student_id
                JOIN routes r ON sr.route_id = r.id
                WHERE r.route_number = %s
            """
            
            cursor.execute(query, (route_number,))
            results = cursor.fetchall()
            
            if results:
                response = f"Students on Route {route_number}:\n"
                for student in results:
                    response += f"- {student['name']} ({student['system_id']})\n"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"No students found for route {route_number}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching student information: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchRouteTiming(Action):
    def name(self) -> Text:
        return "action_fetch_route_timing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            route_number = tracker.get_slot("route_number")
            
            query = """
                SELECT route_number, route_shift, start_time, end_time
                FROM routes
                WHERE route_number = %s
            """
            
            cursor.execute(query, (route_number,))
            result = cursor.fetchone()
            
            if result:
                response = f"Route {result['route_number']} Timing:\n"
                response += f"Shift: {result['route_shift']}\n"
                response += f"Start Time: {result['start_time']}\n"
                response += f"End Time: {result['end_time']}"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find timing information for route {route_number}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching route timing: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchTotalRoutes(Action):
    def name(self) -> Text:
        return "action_fetch_total_routes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT route_number, route_shift, bus_number
                FROM routes
                ORDER BY route_number
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                response = "Available Routes:\n"
                for route in results:
                    response += f"- Route {route['route_number']} ({route['route_shift']}) - Bus {route['bus_number']}\n"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text="No routes found in the system")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching routes: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchRouteByStudentId(Action):
    def name(self) -> Text:
        return "action_fetch_route_by_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            student_id = tracker.get_slot("student_id")
            
            if not student_id:
                dispatcher.utter_message(text="Please provide your student ID.")
                return []
            
            query = """
                SELECT r.route_number, r.route_shift, r.bus_number, r.start_time, r.end_time,
                       d.name as driver_name, d.contact_number, s.name as student_name
                FROM students s
                JOIN student_routes sr ON s.id = sr.student_id
                JOIN routes r ON sr.route_id = r.id
                LEFT JOIN drivers d ON r.id = d.route_id
                WHERE s.system_id = %s
            """
            
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                response = f"Hello {result['student_name']},\n"
                response += f"Your assigned route is {result['route_number']}:\n"
                response += f"Bus Number: {result['bus_number']}\n"
                response += f"Shift: {result['route_shift']}\n"
                response += f"Timing: {result['start_time']} to {result['end_time']}\n"
                if result['driver_name']:
                    response += f"Driver: {result['driver_name']} ({result['contact_number']})"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any route assigned to student ID {student_id}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching route information: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []

class ActionFetchRouteStats(Action):
    def name(self) -> Text:
        return "action_fetch_route_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                dispatcher.utter_message(text="Sorry, I'm having trouble connecting to the database.")
                return []

            cursor = conn.cursor(dictionary=True)
            route_number = tracker.get_slot("route_number")
            
            # Get route details
            route_query = """
                SELECT r.route_number, r.route_shift, r.bus_number,
                       COUNT(DISTINCT sr.student_id) as student_count,
                       d.name as driver_name, d.contact_number
                FROM routes r
                LEFT JOIN student_routes sr ON r.id = sr.route_id
                LEFT JOIN drivers d ON r.id = d.route_id
                WHERE r.route_number = %s
                GROUP BY r.id, r.route_number, r.route_shift, r.bus_number, d.name, d.contact_number
            """
            
            cursor.execute(route_query, (route_number,))
            result = cursor.fetchone()
            
            if result:
                response = f"Route {result['route_number']} Statistics:\n"
                response += f"Shift: {result['route_shift']}\n"
                response += f"Bus Number: {result['bus_number']}\n"
                response += f"Total Students: {result['student_count']}\n"
                if result['driver_name']:
                    response += f"Driver: {result['driver_name']} ({result['contact_number']})"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find statistics for route {route_number}")
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching route statistics: {str(e)}")
        finally:
            close_db_connection(conn, cursor)
        
        return []
