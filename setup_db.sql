-- Create the database and use (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS tkinter_project2;
USE tkinter_project2;

-- Create the users table for authentication
CREATE TABLE IF NOT EXISTS users_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL, 
    contact VARCHAR(255) NOT NULL
);

-- Create the problems table
CREATE TABLE IF NOT EXISTS problems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_Id INT,
    name VARCHAR(255),
    difficulty VARCHAR(50),
    topic VARCHAR(255),
    status VARCHAR(255),
    url VARCHAR(255),
    notes VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the user_progress table for tracking progress
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    problem_id INTEGER,
    solved_date Date,
    difficulty TEXT,
    category TEXT,
    FOREIGN KEY (user_id) REFERENCES users_info(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);
