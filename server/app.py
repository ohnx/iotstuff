import os
from flask import Flask, request, jsonify
app = Flask(__name__)

current_data = None
extra_msg = "hihi"
TEMP_OFFSET = -3

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/set_extra/<extra>")
def get_data2(extra):
    global extra_msg
    extra_msg = extra
    return "ok done"

@app.route("/pub_data/<rawtemp>/<rawgas>/<humidity>/<pressure>", methods=["GET"])
def update_data(rawtemp, rawgas, humidity, pressure):
    global current_data
    current_data = {
        "temp": float(rawtemp) + TEMP_OFFSET,
        "gas": float(rawgas), # TODO: calibration, etc. here
        "humidity": float(humidity),
        "pressure": float(pressure)
    }

    return jsonify({"weather_temp": -105, "weather_type": "sunny", "date": "Sunday January 18, 2023", "extra": extra_msg, "next_update": 60})

@app.route("/data", methods=["GET"])
def fetch_data():
    return jsonify(current_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

