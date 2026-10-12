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
        max_options=MAX_OPTIONS,
        max_rolls=MAX_ROLLS,
        app_title=APP_TITLE,
    )


def form_int(field, default, maximum):
    # Accept thousands separators ("100,000"), fall back to the default on
    # bad input, and keep the value between 1 and the maximum.
    try:
        value = int(request.form[field].replace(",", ""))
    except Exception:
        return default
    return max(1, min(value, maximum))


@app.route("/", methods=["POST"])
def home_post():
    options = form_int("options", DEFAULT_OPTIONS, MAX_OPTIONS)
    rolls = form_int("rolls", DEFAULT_ROLLS, MAX_ROLLS)

    try:
        details = int(request.form["details"])
    except Exception:
        details = 0

    result = str(gjcr.rand(options, rolls, details))

    if details == 1:
        result = result.replace("\n", "<BR>")

    result = result.replace(
        "WINNER!", "<span class='winner'>WINNER!</span>"
    )

    return render_template(
        "home.html", options=options, rolls=rolls, details=details, page_body=result,
        max_options=MAX_OPTIONS, max_rolls=MAX_ROLLS, app_title=APP_TITLE
    )


if __name__ == "__main__":
    app.run()
