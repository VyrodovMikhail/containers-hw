from flask import Flask, jsonify
import psycopg2
import os
import argparse

app = Flask(__name__)

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "app_db"),
    "user": os.getenv("POSTGRES_USER", "app_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "app_password"),
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def save_content_to_db(content: str):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO data (content) VALUES (%s) RETURNING id, created_at",
                    (content,),
                )
                new_id, created_at = cur.fetchone()
        return {"id": new_id, "created_at": str(created_at)}, None
    except Exception as exc:  # pragma: no cover - simple demo logging
        return None, exc


@app.route('/')
def hello():
    return "Hello from Docker!"


@app.route('/data')
def data():
    # Чтение данных из volume
    data_path = '/app/data/example.txt'
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            content = f.read()
        return f"Data from volume: {content}"
    return "No data file found. Create one in /app/data/"

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/db-rows')
def list_rows():
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, content, created_at FROM data ORDER BY id DESC")
                rows = cur.fetchall()
    except Exception as exc:  # pragma: no cover - simple demo logging
        return f"Failed to read from Postgres: {exc}", 500

    parsed = [
        {"id": row[0], "content": row[1], "created_at": str(row[2])}
        for row in rows
    ]
    return jsonify(parsed)

@app.route('/save-to-db')
def save_to_db():
    data_path = '/app/data/example.txt'
    if not os.path.exists(data_path):
        return "No /app/data/example.txt to save. Run init first.", 404

    with open(data_path, 'r') as f:
        content = f.read()

    result, error = save_content_to_db(content)
    if error:
        return f"Failed to save to Postgres: {error}", 500
    return jsonify({"status": "saved", **result})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', type=str)
    args = parser.parse_args()
    # with open(f"{args.output_dir}/output.txt", "w") as f:
    #     f.write("Application was started.")
    app.run(host='0.0.0.0', port=5000)