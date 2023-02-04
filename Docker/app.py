import socket
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    hostname = socket.gethostname()
    return 'Hello User! My container ID: {}\n'.format(hostname)