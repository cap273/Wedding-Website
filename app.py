from flask import Flask, render_template, jsonify, request
import os
import requests

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["PORT"] = 5000

# To be retrieved at runtime
api_key = os.environ.get("airtable_api_key")

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

    # Prepare data for PATCH request against Airtable
    update_record_url = airtable_api_url + "/" + record_id

    if request.json["attending"] == "yes":

        fields_dict = dict()
        fields_dict["Guest Name(s)"] = guest_name
        fields_dict = add_field_to_dict(
            fields_dict, "rsvp_num_guests", request.json, "Number Attending"
        )
        fields_dict = add_field_to_dict(
            fields_dict, "rsvp_beachday", request.json, "Attending Wednesday Beach Day"
        )
        fields_dict = add_field_to_dict(
            fields_dict, "rsvp_wednesdaywelcomedinner", request.json, "Attending Wednesday Welcome Dinner"
        )
        fields_dict = add_field_to_dict(
            fields_dict,
            "rsvp_weddingevedinner",
            request.json,
            "Attending Wedding Eve Dinner",
        )
        fields_dict = add_field_to_dict(
            fields_dict,
            "rsvp_postweddingbrunch",
            request.json,
            "Attending Post Wedding Brunch",
        )
        fields_dict = add_field_to_dict(
            fields_dict, "primary_email", request.json, "Primary Email"
        )
        fields_dict = add_field_to_dict(
            fields_dict, "secondary_email", request.json, "Secondary Email"
        )
        fields_dict = add_field_to_dict(
            fields_dict, "dietary_restrictions", request.json, "Dietary Restrictions"
        )
        fields_dict = add_field_to_dict(fields_dict, "hotels", request.json, "Hotels")

        fields_dict = add_field_to_dict(fields_dict, "flights_arrival_date", request.json, "Flight Arrival Date")
        fields_dict = add_field_to_dict(fields_dict, "flights_arrival_time", request.json, "Flight Arrival Time")
        fields_dict = add_field_to_dict(fields_dict, "arrival_flight", request.json, "Flight Arrival Number")
        fields_dict = add_field_to_dict(fields_dict, "flights_departure_date", request.json, "Flight Departure Date")
        fields_dict = add_field_to_dict(fields_dict, "flights_departure_time", request.json, "Flight Departure Time")
        fields_dict = add_field_to_dict(fields_dict, "departure_flight", request.json, "Flight Departure Number")

        fields_dict = add_field_to_dict(
            fields_dict, "message", request.json, "Message From Guests"
        )

        # Necessity for "typecast" attribute: https://dev.to/markokolombo/airtable-post-patch-errors-solved-3fkd
        record_update = {
            "fields": fields_dict,
            "typecast": True,
        }

    else:

        fields_dict = dict()
        fields_dict["Guest Name(s)"] = guest_name
        fields_dict = add_field_to_dict(
            fields_dict, "rsvp_num_guests", request.json, "Number Attending"
        )
        fields_dict = add_field_to_dict(
            fields_dict, "message", request.json, "Message From Guests"
        )

        record_update = {
            "fields": fields_dict,
            "typecast": True,
        }

    # Execute PATCH request
    response = requests.patch(
        update_record_url, json=record_update, headers=create_http_header()
    )

    if "id" not in response.json() or response.json()["id"] != record_id:
        print("Error: JSON response below:")
        print(response.json())
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
    guest_name = guest_name.replace("[", "%5B")
    guest_name = guest_name.replace("]", "%5D")

    return guest_name


def add_field_to_dict(fields_dict, field_name, request_dict, airtable_column_name):

    if (
        field_name in request_dict
        and request_dict[field_name] is not None
        and request_dict[field_name] != ""
    ):

        if airtable_column_name.startswith("Attending "):
            if request_dict[field_name] == "yes":
                fields_dict[airtable_column_name] = "Attending"
            else:
                fields_dict[airtable_column_name] = "Not Attending"
        else:
            fields_dict[airtable_column_name] = request.json[field_name]

    return fields_dict


# -------------------------------- Main Execution ------------------------------

if __name__ == "__main__":

    # Run app in debug mode
    # app.run(host="localhost", port=int(app.config["PORT"]), debug=True)

    app.run(debug=True)
