-- V2: Add admin role and default admin user

START TRANSACTION;

ALTER TABLE users MODIFY COLUMN role ENUM('student', 'admin') NOT NULL DEFAULT 'student';

INSERT IGNORE INTO users (email, password_hash, role) VALUES
  ('admin@internhub.local', '$2b$12$lhsZu.oxivJ9a.SQCPAy9OsmD8ALLq/ZcYMOhauJqHly8o8WPm592', 'admin');
-- IMPORTANT: Change admin password immediately after first login

COMMIT;
