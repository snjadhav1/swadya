CREATE DATABASE event_db1;

USE event_db1;

DROP TABLE IF EXISTS registrations;

CREATE TABLE registrations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  mobile VARCHAR(20) NOT NULL,
  role VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email (email),
  INDEX idx_created_at (created_at),
  INDEX idx_role (role)
);


-- Sample data for development / testing
INSERT INTO registrations (name, email, mobile, role, password, created_at) VALUES
  ('Ram Kumar', 'ram.kumar@example.com', '9123456789', 'helpseeker', 'password123', '2025-11-01 10:00:00'),
  ('Sita Patil', 'sita.patil@example.com', '9012345678', 'volunteer', 'volunteerpass', '2025-11-02 11:30:00'),
  ('Mira Joshi', 'mira.joshi@example.com', '9988776655', 'helpseeker', 'securepwd', '2025-11-03 09:00:00');

-- Verify table contents
SELECT * FROM registrations LIMIT 10;