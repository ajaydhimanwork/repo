from flask import Flask, request
import pyodbc
import os

app = Flask(__name__)

@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()

    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('svlicense.wizoneit.com,1440')};"
        f"DATABASE={os.getenv('TestingSheet')};"
        f"UID={os.getenv('sa')};PWD={os.getenv('ss123456')}"
    )

    cursor = conn.cursor()
    cursor.execute(
        "MERGE INTO SheetData AS target USING (SELECT ? AS id, ? AS name, ? AS email) AS src " +
        "ON target.id = src.id " +
        "WHEN MATCHED THEN UPDATE SET name = src.name, email = src.email " +
        "WHEN NOT MATCHED THEN INSERT (id, name, email) VALUES (src.id, src.name, src.email);",
        data['id'], data['name'], data['email']
    )
    conn.commit()
    return "OK", 200
