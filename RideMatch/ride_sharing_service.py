import requests
from flask import Flask, request
import apscheduler.schedulers.background
import redis
import json

app = Flask(__name__)

flag = False

rdb = None


def get_distance(p1, p2):
    temp = pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)
    return pow(temp, 0.5)


def format_list(li: list):
    temp = []
    for i in li:
        i = str(i)
        i = i.lstrip('b').strip("'")
        i = json.loads(i)
        temp.append(i)
    return temp


def client_match():
    if not flag:
        return

    avail_rider = rdb.lrange('riders', 0, -1)
    print('.................AVAIL RIDER................')
    print(avail_rider)
    avail_rider = format_list(avail_rider)

    avail_driver = rdb.lrange('drivers', 0, -1)
    print('.................AVAIL Driver................')
    print(avail_driver)
    avail_driver = format_list(avail_driver)

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

        if rider['loc'][0] < 51:
            requests.post("http://communication_service_dhaka:8080/comm", json=notification)
        else:
            requests.post("http://communication_service_chittagong:8080/comm", json=notification)

        avail_rider.remove(rider)
        rdb.delete('riders')
        for i in avail_rider:
            rdb.rpush('riders', json.dumps(i))

        avail_driver.remove(sel_driver)
        rdb.delete('drivers')
        for i in avail_driver:
            rdb.rpush('drivers', json.dumps(i))


schedule = apscheduler.schedulers.background.BackgroundScheduler()
schedule.add_job(func=client_match, trigger="interval", seconds=5)
schedule.start()


@app.route("/api/rider", methods=["POST"])
def rider_update():
    data = request.json

    global flag, rdb
    flag = True

    if not flag and data['loc'][0] < 51:
        rdb = redis.Redis(host='redis_container_dhaka', port=6379)
    else:
        rdb = redis.Redis(host='redis_container_chittagong', port=6379)

    print("message received from client :", data)
    data = json.dumps(data)

    rdb.rpush('riders', data)

    return "Rider Api received by Server"


@app.route("/api/driver", methods=["POST"])
def driver_update():
    data = request.json
    print("message received from client :", data)
    data = json.dumps(data)

    global rdb
    rdb.rpush('drivers', data)

    return "Driver Api received by Server"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
