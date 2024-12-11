from flask import Flask
import psycopg2
import random
from datetime import datetime

# database connection
db_params = {
"dbname": "postgres",
"user": "user",
"password": "password",
"host": "postgres",
"port": "5432"
}

app = Flask(__name__)

def increment_counter():
  conn = None
  try:
  #database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    print("before select")
    cursor.execute("SELECT counter FROM refresh_counter;")
    print("After select")
    cursor.execute("SELECT COUNT(*) FROM refresh_counter;")
    if cursor.fetchone()[0] == 0:
      cursor.execute("INSERT INTO refresh_counter (counter) VALUES (0);")

    cursor.execute("UPDATE refresh_counter SET counter = counter +1;")
    cursor.execute("SELECT counter FROM refresh_counter;")
    current_counter = cursor.fetchone()[0]

  #commit
    conn.commit()
    print(f"current  counter has been increased, value: {current_counter}")
    return current_counter

  except Exception as e:
    print(f"Error : {e}")
  finally:
    if conn:
      cursor.close()
      conn.close()

def read_file():
  file_path = '/app/special/special.properties'
  try:
    with open(file_path, 'r') as file:
      content = file.read()
      return content
  except Exception as e:
    return f"An error happened: {e}"

@app.route('/')
def random_number():
  number = random.randint(1,20)
  current_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  content = read_file()
  counter = increment_counter()
  return f"Output: {number}:{current_date}:{content}:views:{counter}"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
