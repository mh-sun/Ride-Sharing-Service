from flask import Flask, request
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'its secret'

app.config['MONGODB_SETTINGS'] = {
    'db': 'driver_data',
    'host': 'mongodb_container',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


class Rating(db.Document):
    rider = db.StringField()
    driver = db.StringField()
    rating = db.IntField()


def insert_into_database(rider, driver, rate):
    rate_info = Rating(rider=rider, driver=driver, rating=rate)
    rate_info.save()


@app.route("/rating", methods=["POST"])
def rating():
    data = request.json
    print("\n\nGOT DATA FROM CLIENT\n\n\n", data, "IS INSERTED............")
    insert_into_database(data['rname'], data['dname'], data['rate'])
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
