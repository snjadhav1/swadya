-- Create database
CREATE DATABASE IF NOT EXISTS digital_literacy;
USE digital_literacy;

-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    venue VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin (username: admin, password: admin123)
INSERT INTO admins (username, password) VALUES 
('admin', 'admin123');

-- Insert sample sessions
INSERT INTO sessions (title, category, date, venue, description) VALUES
('Computer Basics for Beginners', 'Computer Basics', '2025-11-20', 'Community Center', 'Learn the fundamentals of using a computer'),
('Smartphone Essentials', 'Smartphone Help', '2025-11-22', 'Public Library', 'Master your smartphone basics'),
('Internet Safety Workshop', 'Internet Safety', '2025-11-25', 'Computer Lab', 'Stay safe online');
