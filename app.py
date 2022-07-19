from flask import Flask, render_template, request, jsonify
import os
import configparser


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["PORT"] = 5000

# -------------------------------- Web Routes ----------------------------------

# Index/home routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def default(path=None):
    return render_template("index.html")

# Index/home routes
@app.route("/es", defaults={"path": ""})
@app.route("/es/<path:path>")
def default_es(path=None):
    return render_template("es/index.html")


# -------------------------------- API Routes ----------------------------------


# -------------------------------- Main Execution ------------------------------

if __name__ == "__main__":

    # Run app in debug mode
    app.run(host="localhost", port=int(app.config["PORT"]), debug=True)
