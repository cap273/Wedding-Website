from flask import Flask, render_template, jsonify, request
import os
import requests
import json

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["PORT"] = 5000

# To be retrieved at runtime
api_key = os.environ.get('airtable_api_key')

airtable_api_url = (
    "https://api.airtable.com/v0/appAvSmZJGheuZgRf/Guests%20by%20Grouping"
)

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
    return jsonify({"testName": "testValue"})


@app.route("/getNameRecords", methods=["GET"])
def get_records():

    # Initialize list of guest names
    guest_names = []

    # Execute first GET request against Airtable records, of which a maximum of 100 records will be returned
    response = requests.get(
        airtable_api_url + "?fields%5B%5D=fld0MW4ubneFwzQvq",
        headers=create_http_header(),
    )

    # Add guest names to list
    for record in response.json()["records"]:
        guest_name = record["fields"]["Guest Name(s)"]
        guest_names.append(guest_name)

    # guest_names += list(map(lambda x: x['fields']['Guest Name(s)'], response.json().items()))

    while "offset" in response.json():
        offset_id = response.json()["offset"]

        # Execute another request using offset to get all the records
        response = requests.get(
            airtable_api_url + "?fields%5B%5D=fld0MW4ubneFwzQvq&offset=" + offset_id,
            headers=create_http_header(),
        )

        for record in response.json()["records"]:
            guest_name = record["fields"]["Guest Name(s)"]
            guest_names.append(guest_name)

    return jsonify(guest_names)


@app.route("/submitRsvp", methods=["POST"])
def update_record():

    # Get guest name from the body of the HTTP POST request
    guest_name = request.json["guest_name"]

    # Create URL to retrieve the record that matches a guest name
    get_record_url = (
        airtable_api_url
        + "?filterByFormula=(%7BGuest+Name(s)%7D+%3D+'"
        + encode_guest_name(guest_name)
        + "')"
    )

    # Execute GET request against Airtable to get the record containing this guest name
    response = requests.get(
        get_record_url,
        headers=create_http_header(),
    )

    print(response.json())

    if len(response.json()["records"]) != 1:
        return jsonify(
            {
                "Status": "Error",
                "Message": "Expected a single record. Instead retrieved: "
                + str(len(response.json()["records"])),
            }
        )

    if response.json()["records"][0]["fields"]["Guest Name(s)"] != guest_name:
        return jsonify(
            {
                "Status": "Error",
                "Message": "Retrieved record name does not match. Retrieved: "
                + str(response.json()["records"][0]["fields"]["Guest Name(s)"]),
            }
        )

    record_id = response.json()["records"][0]["id"]
    max_headcount = int(response.json()["records"][0]["fields"]["Max Headcount"])


    # Prepare data for PATCH request against Airtable
    update_record_url = airtable_api_url + "/" + record_id

    if request.json["attending"] == "yes":
        
        # Necessity for "typecast" attribute: https://dev.to/markokolombo/airtable-post-patch-errors-solved-3fkd
        record_update = {
            "fields": {
                "Guest Name(s)": guest_name,
                "Number Attending": request.json["rsvp_num_guests"],
                "Attending Wednesday Beach Day": "Attending" if request.json["rsvp_beachday"] == "yes" else "Not Attending",
                "Attending Wedding Eve Dinner": "Attending" if request.json["rsvp_weddingevedinner"] == "yes" else "Not Attending",
                "Attending Post Wedding Brunch": "Attending" if request.json["rsvp_postweddingbrunch"] == "yes" else "Not Attending",
                "Primary Email": request.json["primary_email"],
                "Secondary Email": request.json["secondary_email"],
                "Dietary Restrictions": request.json["dietary_restrictions"],
                "Flights": request.json["flights"],
                "Hotels": request.json["hotels"],
                "Message From Guests": request.json["message"]
            },
            "typecast": True,
        }

    else:
        record_update = {
            "fields": {
                "Guest Name(s)": guest_name,
                "Number Attending": request.json["rsvp_num_guests"],
                "Message From Guests": request.json["message"]
            },
            "typecast": True,
        }

    # Execute PATCH request
    response = requests.patch(
        update_record_url, json=record_update, headers=create_http_header()
    )

    if response.json()["id"] != record_id:
        return jsonify({"Status": "Error", "Message": "Incorrect record ID returned"})

    if int(response.json()["fields"]["Number Attending"]) != int(
        request.json["rsvp_num_guests"]
    ):
        return jsonify(
            {
                "Status": "Error",
                "Message": "Number attending mismatch. Expected: "
                + str(request.json["rsvp_num_guests"])
                + ". Retrieved: "
                + str(response.json()["fields"]["Number Attending"]),
            }
        )

    return jsonify({"Status": "OK", "Message": "Record updated successfully."})


# -------------------------------- Auxilliary functions ------------------------


def get_single_record():
    return None


def create_http_header():
    headers = dict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + api_key

    return headers


def encode_guest_name(guest_name):

    # Spaces
    guest_name = guest_name.replace(" ", "+")

    # ñ
    guest_name = guest_name.replace("ñ", "%C3%B1")
    guest_name = guest_name.replace("Ñ", "%C3%91o")

    # &
    guest_name = guest_name.replace("&", "%26")

    # ,
    guest_name = guest_name.replace(",", "%2C")

    # accents
    guest_name = guest_name.replace("á", "%C3%A1")
    guest_name = guest_name.replace("é", "%C3%A9")
    guest_name = guest_name.replace("í", "%C3%AD")
    guest_name = guest_name.replace("ó", "%C3%B3")
    guest_name = guest_name.replace("ú", "%C3%BA")

    # []
    guest_name = guest_name.replace("[", '%5B')
    guest_name = guest_name.replace("]", '%5D')

    return guest_name


# -------------------------------- Main Execution ------------------------------

if __name__ == "__main__":

    # Run app in debug mode
    # app.run(host="localhost", port=int(app.config["PORT"]), debug=True)

    app.run(debug=True)
