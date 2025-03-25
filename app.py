from flask import Flask, request
import pyodbc
import os

app = Flask(__name__)

@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};PWD={os.getenv('DB_PASS')}"
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1440))
    app.run(host="svlicense.wizoneit.com", port=port)
