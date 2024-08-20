from flask import Flask, render_template
from rq import Queue
from worker import conn
from tasks import fetch_and_format_lines
from dotenv import load_dotenv
import time
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    api_key = os.getenv('API_KEY')  # Ensure API keys and other env variables are loaded correctly

    # Create a queue
    q = Queue('my_custom_queue', connection=conn)

    # Enqueue the task
    job = q.enqueue(fetch_and_format_lines, api_key)
    print(f"Enqueued job to queue: {q.name}")
    print(f"Job ID: {job.id}")
    print(f"Job Status: {job.get_status()}")

    while not job.is_finished:
        time.sleep(1)

    original_lines = job.return_value()
    print(original_lines)
    print(type(original_lines))

    font_sizes = [85, 70, 50, 45, 30, 20, 15, 13, 10, 8, 8]
    return render_template('index.html', lines=original_lines, font_sizes=font_sizes)

if __name__ == '__main__':
    app.run(debug=True)
