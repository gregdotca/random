#!/usr/bin/env python3
from flask import Flask, render_template, request
from gjcode import rand as gjcr

APP_TITLE = "Randomizer"
default_options = 2
default_rolls = 100000
default_details = 1
max_options = 1000
max_rolls = 1000000

app = Flask(__name__, static_folder="assets")


@app.route("/")
def home():
    return render_template(
        "home.html",
        options=default_options,
        rolls=default_rolls,
        details=default_details,
        app_title=APP_TITLE,
    )


@app.route("/", methods=["POST"])
def home_post():

    try:
        options = int(request.form["options"])
    except Exception:
        options = default_options

    try:
        rolls = int(request.form["rolls"])
    except Exception:
        rolls = default_rolls

    try:
        details = int(request.form["details"])
    except Exception:
        details = 0

    if options > max_options:
        options = max_options

    if rolls > max_rolls:
        rolls = max_rolls

    result = str(gjcr.rand(options, rolls, details))

    if details == 1:
        result = result.replace("\n", "<BR>")

    result = result.replace(
        "WINNER!", "<span style='color: red; font-weight: bold;'>WINNER!</span>"
    )

    return render_template(
        "home.html", options=options, rolls=rolls, details=details, page_body=result, app_title=APP_TITLE
    )


if __name__ == "__main__":
    app.run()
