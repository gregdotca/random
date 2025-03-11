#!/usr/bin/env python3
from flask import Flask, render_template, request
from gjcode import rand as gjcr

APP_TITLE = "Randomizer"
DEFAULT_OPTIONS = 2
DEFAULT_ROLLS = 100000
DEFAULT_DETAILS = 1
MAX_OPTIONS = 1000
MAX_ROLLS = 1000000

app = Flask(__name__, static_folder="assets")


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "home.html",
        options=DEFAULT_OPTIONS,
        rolls=DEFAULT_ROLLS,
        details=DEFAULT_DETAILS,
        app_title=APP_TITLE,
    )


@app.route("/", methods=["POST"])
def home_post():
    try:
        options = int(request.form["options"])
    except Exception:
        options = DEFAULT_OPTIONS

    try:
        rolls = int(request.form["rolls"])
    except Exception:
        rolls = DEFAULT_ROLLS

    try:
        details = int(request.form["details"])
    except Exception:
        details = 0

    if options > MAX_OPTIONS:
        options = MAX_OPTIONS

    if rolls > MAX_ROLLS:
        rolls = MAX_ROLLS

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
