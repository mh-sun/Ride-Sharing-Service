from flask import Flask, request, g
from flask_socketio import SocketIO, emit
import json, eventlet


eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'its secret'
sio = SocketIO(app)


@app.route("/comm", methods=["POST"])
def send_pair():
    info = request.json
    print("message received from ride-share :", info)
    print('Sendind data to client')
    sio.emit("notify", info)
    return "Communication received from ride share"


if __name__ == '__main__':
    print("Communication Started")
    sio.run(app, host='0.0.0.0', port=8080)
