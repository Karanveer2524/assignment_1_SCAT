import os
import pymysql
from urllib.request import urlopen
import requests
import subprocess
import shlex

# Hardcoded Credentials (db_config dictionary)
# Vulnerability: The database credentials (host, user, password) are hardcoded in the script, making them easily accessible if the source code is leaked.
# OWASP Category: A02:2021 – Cryptographic Failures
# Mitigation: Store credentials in environment variables or a secure secrets management system.

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

# Command Injection via os.system in send_email
# Vulnerability: The os.system function is used to construct a shell command with user-supplied data (body and subject), which can allow command injection.
# OWASP Category: A03:2021 – Injection
# Mitigation: Use a safer approach such as Python’s built-in subprocess.run with shlex.quote().

def send_email(to, subject, body):
    command = f'echo {shlex.quote(body)} | mail -s {shlex.quote(subject)} {shlex.quote(to)}'
    subprocess.run(command, shell=True, check=True)

# Unvalidated External URL in get_data
# Vulnerability: The script fetches data from http://insecure-api.com/get-data without validating the source or using HTTPS.
# OWASP Category: A08:2021 – Software and Data Integrity Failures
# Mitigation: Use HTTPS and validate the SSL certificate.
def get_data():
    url = 'https://secure-api.com/get-data'  # Use HTTPS
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise error for bad responses
    return response.text

# SQL Injection in save_to_db
# Vulnerability: The SQL query is built using string concatenation, allowing SQL injection if data contains malicious SQL code.
# OWASP Category: A03:2021 – Injection
# Mitigation: Use parameterized queries.

def save_to_db(data):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
