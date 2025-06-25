from flask import Flask, render_template, request
# import pymssql  # pymssql works with both Azure SQL and AWS SQL Server
import pymysql

app = Flask(__name__)

# Replace these with your actual AWS RDS SQL Server values
AWS_RDS_SQL_SERVER = 'cicd-testdb.can8amiomg45.us-east-1.rds.amazonaws.com'
DB_PORT=3306
AWS_RDS_SQL_USERNAME = 'admin'
AWS_RDS_SQL_PASSWORD = 'AWS$12345'
AWS_RDS_SQL_DATABASE = "cicd_testdb"


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']

    if not name or not message:
        return "Name and message are required.", 400

    try:
        # Connect to AWS RDS SQL Server using pymssql
        conn = pymysql.connect(
            host=AWS_RDS_SQL_SERVER,
            port=DB_PORT,
            user=AWS_RDS_SQL_USERNAME,
            password=AWS_RDS_SQL_PASSWORD,
            database=AWS_RDS_SQL_DATABASE
            
        )
        cursor = conn.cursor()

        # Ensure the table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            message TEXT
            );
        """)

        # Insert data
        cursor.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()

        cursor.close()
        conn.close()
        return "Message submitted successfully!"

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
