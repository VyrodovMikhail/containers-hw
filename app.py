from flask import Flask
import os
import argparse

app = Flask(__name__)


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', type=str)
    args = parser.parse_args()
    with open(f"{args.output_dir}/output.txt", "w") as f:
        f.write("Application was started.")
    app.run(host='0.0.0.0', port=5000)