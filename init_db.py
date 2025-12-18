import os
import psycopg2
import time

time.sleep(2)

print("Start script")

conn = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)

cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS data (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
''')
print("Table created")

cur.execute('''
    INSERT INTO data (content) VALUES ('Some text');
''')


conn.commit()
cur.close()
conn.close()

print("Database initialized successfully")