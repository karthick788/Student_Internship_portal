-- ============================================================
-- InternHub — PlanetScale-Compatible Schema
-- ============================================================
-- IMPORTANT: PlanetScale (Vitess) does NOT enforce FOREIGN KEY
-- constraints. All FK CONSTRAINT lines have been removed.
-- UNIQUE KEY constraints are fully supported and kept.
-- Referential integrity is enforced at the application layer.
-- ============================================================
-- HOW TO IMPORT:
--   1. In PlanetScale dashboard → your database → Branches → main
--   2. Click "Console" → paste and run this file section by section
--   OR use: pscale shell <db_name> main < database_planetscale.sql
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('student', 'admin') NOT NULL DEFAULT 'student',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  full_name VARCHAR(150) NOT NULL,
  phone VARCHAR(20) NULL,
  college VARCHAR(200) NULL,
  course VARCHAR(150) NULL,
  year_of_study VARCHAR(40) NULL,
  city VARCHAR(100) NULL,
  bio TEXT NULL,
  date_of_birth DATE NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS education (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  institution VARCHAR(200) NOT NULL,
  degree VARCHAR(120) NOT NULL,
  field_of_study VARCHAR(150) NULL,
  start_year INT NULL,
  end_year INT NULL,
  grade VARCHAR(40) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS student_skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  skill_id INT NOT NULL,
  UNIQUE KEY uq_student_skill (student_id, skill_id)
);

CREATE TABLE IF NOT EXISTS resumes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  stored_name VARCHAR(255) NOT NULL,
  original_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  mime_type VARCHAR(120) NOT NULL,
  file_size INT NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  external_id VARCHAR(191) NULL,
  source VARCHAR(80) NOT NULL DEFAULT 'manual',
  title VARCHAR(255) NOT NULL,
  company_name VARCHAR(200) NOT NULL,
  description TEXT NULL,
  location VARCHAR(150) NULL,
  work_mode ENUM('remote', 'onsite', 'hybrid') NOT NULL DEFAULT 'onsite',
  skills VARCHAR(500) NULL,
  duration VARCHAR(80) NULL,
  stipend VARCHAR(80) NULL,
  eligibility TEXT NULL,
  deadline DATE NULL,
  application_method ENUM('internal', 'external') NOT NULL DEFAULT 'external',
  application_url VARCHAR(1000) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_internship_source_ext (source, external_id)
);

CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  application_code VARCHAR(32) NOT NULL UNIQUE,
  student_id INT NOT NULL,
  internship_id INT NOT NULL,
  status ENUM('submitted', 'under_review', 'shortlisted', 'rejected', 'selected') NOT NULL DEFAULT 'submitted',
  cover_note TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_student_internship (student_id, internship_id)
);

CREATE TABLE IF NOT EXISTS saved_internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  internship_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_saved (student_id, internship_id)
);

CREATE TABLE IF NOT EXISTS notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  is_read TINYINT(1) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS linkedin_internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  company_name VARCHAR(200) NOT NULL,
  location VARCHAR(150) NULL,
  description TEXT NULL,
  skills VARCHAR(500) NULL,
  linkedin_url VARCHAR(1000) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Seed Data
-- ============================================================

INSERT INTO internships
  (external_id, source, title, company_name, description, location, work_mode, skills, duration, stipend, eligibility, deadline, application_method, application_url)
VALUES
  ('seed-1', 'seed', 'Python Developer Intern', 'Nimbus Labs',
   'Work on Flask APIs, data pipelines, and internship matching features. You will collaborate with mentors on real product work.',
   'Bangalore', 'hybrid', 'Python, Flask, MySQL, REST APIs', '3 months', '₹15,000 / month',
   'Undergraduate students with basic Python knowledge.', '2026-10-31', 'internal', NULL),
  ('seed-2', 'seed', 'Frontend Web Intern', 'PixelForge Studio',
   'Build responsive student-facing interfaces with HTML, CSS, and JavaScript. Focus on accessibility and mobile layouts.',
   'Chennai', 'onsite', 'HTML, CSS, JavaScript', '2 months', '₹10,000 / month',
   'Students comfortable with HTML/CSS/JS.', '2026-09-30', 'internal', NULL),
  ('seed-3', 'seed', 'Data Analytics Intern', 'InsightWave',
   'Clean datasets, build dashboards, and summarize internship market trends for internal research.',
   'Hyderabad', 'remote', 'Python, SQL, Excel, Data Analysis', '3 months', '₹12,000 / month',
   'Any degree with statistics or CS coursework.', '2026-11-15', 'internal', NULL),
  ('seed-4', 'seed', 'UI/UX Design Intern', 'Harbor Design Co.',
   'Create wireframes and visual systems for a student career platform. Portfolio review required.',
   'Pune', 'hybrid', 'Figma, UI Design, Prototyping', '2 months', '₹8,000 / month',
   'Design students or self-taught designers with a portfolio.', '2026-10-20', 'internal', NULL),
  ('seed-5', 'seed', 'Cloud Support Intern', 'Skyline Cloud',
   'Assist with AWS basics, documentation, and monitoring dashboards for internal tools.',
   'Mumbai', 'onsite', 'Linux, AWS, Networking', '6 months', '₹20,000 / month',
   'Engineering students in 3rd or 4th year.', '2026-12-01', 'internal', NULL),
  ('seed-6', 'seed', 'Software Engineering Intern', 'Remotive Sample Org',
   'This listing demonstrates an external apply flow. You will be sent to the original application page.',
   'Remote', 'remote', 'JavaScript, Python', '3 months', 'Unpaid / stipend varies',
   'Open to students worldwide.', '2026-10-10', 'external', 'https://remotive.com/remote-jobs/software-dev');

INSERT INTO linkedin_internships (title, company_name, location, description, skills, linkedin_url) VALUES
  ('Software Engineering Intern', 'Various companies on LinkedIn', 'India',
   'Official LinkedIn job search for software internships in India. Opens LinkedIn — this platform does not scrape LinkedIn.',
   'Software Engineering, Programming',
   'https://www.linkedin.com/jobs/search/?keywords=software%20intern&location=India'),
  ('Data Science Intern', 'Various companies on LinkedIn', 'Bangalore',
   'LinkedIn search for data science internships in Bangalore.',
   'Python, Machine Learning, SQL',
   'https://www.linkedin.com/jobs/search/?keywords=data%20science%20intern&location=Bengaluru%2C%20Karnataka%2C%20India'),
  ('Marketing Intern', 'Various companies on LinkedIn', 'Remote',
   'LinkedIn search for remote marketing internships.',
   'Marketing, Communication',
   'https://www.linkedin.com/jobs/search/?keywords=marketing%20intern&f_WT=2'),
  ('Mechanical Engineering Intern', 'Various companies on LinkedIn', 'Chennai',
   'LinkedIn search for mechanical internships in Chennai.',
   'CAD, Mechanical Engineering',
   'https://www.linkedin.com/jobs/search/?keywords=mechanical%20intern&location=Chennai%2C%20Tamil%20Nadu%2C%20India'),
  ('Product Management Intern', 'Various companies on LinkedIn', 'Hyderabad',
   'LinkedIn search for product management intern roles.',
   'Product, Research, Communication',
   'https://www.linkedin.com/jobs/search/?keywords=product%20management%20intern&location=Hyderabad');

INSERT INTO skills (name) VALUES
  ('Python'), ('JavaScript'), ('HTML'), ('CSS'), ('MySQL'), ('Flask'),
  ('Java'), ('C++'), ('SQL'), ('Figma'), ('React'), ('Data Analysis')
ON DUPLICATE KEY UPDATE name = VALUES(name);
