import requests
from flask import Flask, request
import apscheduler.schedulers.background

app = Flask(__name__)

avail_rider = []
avail_driver = []


def get_distance(p1, p2):
    temp = pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)
    return pow(temp, 0.5)


def client_match():
    if not avail_driver or not avail_rider:
        return
    for rider in avail_rider:
        if not avail_driver or not avail_rider:
            return
        mini = 500000
        sel_driver = None

        for driver in avail_driver:
            if get_distance(rider["loc"], driver["loc"]) < mini:
                sel_driver = driver

        fare = get_distance(rider['loc'], rider['des']) * 2

        notification = {
            'r_name': rider['name'],
            'd_name': sel_driver['name'],
            'fare': fare
        }
        print("Server has paired rider %s with driver %s" %
              (rider['name'], sel_driver['name']))
        print("message sending to comm :", notification)
        requests.post("http://communication_service:8080/comm", json=notification)

        avail_rider.remove(rider)
        avail_driver.remove(sel_driver)


schedule = apscheduler.schedulers.background.BackgroundScheduler()
schedule.add_job(func=client_match, trigger="interval", seconds=5)
schedule.start()


@app.route("/api/rider", methods=["POST"])
def rider_update():
    data = request.json
    print("message received from client :", data)
    avail_rider.append(data)
    return "Rider Api received by Server"


@app.route("/api/driver", methods=["POST"])
def driver_update():
    data = request.json
    print("message received from client :", data)
    avail_driver.append(data)
    return "Driver Api received by Server"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
