import os
import sys

# ensure we can import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
import mysql.connector

conn = mysql.connector.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
    ssl_ca=Config.DB_SSL_CA if Config.DB_SSL_CA else None
)
cursor = conn.cursor()
cursor.execute("ALTER TABLE applications MODIFY COLUMN status ENUM('submitted', 'under_review', 'shortlisted', 'rejected', 'selected', 'student_selected_next_round', 'student_rejected', 'student_applied') NOT NULL DEFAULT 'submitted';")
conn.commit()
print("Success")
