-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS transport_management;
USE transport_management;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS student_routes;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS routes;

-- Create routes table
CREATE TABLE routes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    route_number VARCHAR(50) NOT NULL,
    route_shift VARCHAR(50),
    bus_number VARCHAR(50),
    start_time TIME DEFAULT '07:00:00',
    end_time TIME DEFAULT '17:00:00',
    UNIQUE KEY unique_route (route_number)
);

-- Create drivers table
CREATE TABLE drivers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20),
    route_id INT,
    FOREIGN KEY (route_id) REFERENCES routes(id)
);

-- Create students table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    system_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    semester VARCHAR(20),
    UNIQUE KEY unique_system_id (system_id)
);

-- Create student_routes table for mapping students to routes
CREATE TABLE student_routes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    route_id INT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (route_id) REFERENCES routes(id),
    UNIQUE KEY unique_student_route (student_id, route_id)
); 