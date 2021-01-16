import os

import flask

app = flask.Flask(__name__)


@app.route("/")
def test():
    return "/"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run("0.0.0.0", port)
