from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import configparser
import requests

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["PORT"] = 5000

# To be retrieved at runtime
api_key = os.environ.get('airtable_api_key')

# -------------------------------- Web Routes ----------------------------------

# Index/home routes
@app.route("/")
@app.route("/<path:path>")
def default(path=None):
    return render_template("index.html")

# Index/home routes
@app.route("/es")
@app.route("/es/<path:path>")
def default_es(path=None):
    return render_template("es/index.html")


# -------------------------------- API Routes ----------------------------------

@app.route("/test", methods=["GET"])
def get_api():
    return jsonify(
        {"testName": "testValue"}
    )

@app.route("/getNameRecords", methods=["GET"])
def get_records():

    # Headers for API request to Airtable
    headers = dict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + api_key

    # Initialize list of guest names
    guest_names = []

    # Execute first GET request against Airtable records, of which a maximum of 100 records will be returned
    response = requests.get(
            "https://api.airtable.com/v0/appAvSmZJGheuZgRf/Guests%20by%20Grouping?fields%5B%5D=fld0MW4ubneFwzQvq", 
            headers=headers
            )

    print(response.json())
    
    # Add guest names to list
    for record in response.json()['records']:
        guest_name = record['fields']['Guest Name(s)']
        guest_names.append(guest_name)
    
    # guest_names += list(map(lambda x: x['fields']['Guest Name(s)'], response.json().items()))

    while 'offset' in response.json():
        offset_id = response.json()['offset']

        # Execute another request using offset to get all the records
        response = requests.get(
            "https://api.airtable.com/v0/appAvSmZJGheuZgRf/Guests%20by%20Grouping?fields%5B%5D=fld0MW4ubneFwzQvq&offset="+offset_id, 
            headers=headers
        )

        for record in response.json()['records']:
            guest_name = record['fields']['Guest Name(s)']
            guest_names.append(guest_name)

    return jsonify(
        guest_names
    )
    
# -------------------------------- Main Execution ------------------------------

if __name__ == "__main__":

    # Run app in debug mode
    # app.run(host="localhost", port=int(app.config["PORT"]), debug=True)

    app.run(debug=True)
