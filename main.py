import os

import flask
import opentok

OPENTOK_API_KEY = "***REMOVED***"
OPENTOK_API_SECRET = "***REMOVED***"

api_opentok = opentok.OpenTok(OPENTOK_API_KEY, OPENTOK_API_SECRET)
app = flask.Flask(__name__)


@app.route("/")
def test():
    return "i despise existence with a fervent passion"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run("0.0.0.0", port)
