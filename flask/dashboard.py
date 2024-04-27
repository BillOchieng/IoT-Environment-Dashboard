from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # print(type(msg.payload))
    socketio.emit(
        "my_response", {"topic": msg.topic, "data": msg.payload.decode("utf-8")}
    )


url = "23ee2ffd9a224d23a9e4e4c0dcbc110b.s1.eu.hivemq.cloud"


def background_thread():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.tls_set()
    mqttc.username_pw_set(username="Bill_IoT", password="Bill_ioT@11")

    mqttc.connect(url, 8883, 60)

    mqttc.loop_forever()


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


@socketio.event
def my_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": message["data"], "count": session["receive_count"]})


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit("my_response", {"data": "Connected", "count": 0})


if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)
