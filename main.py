import os

import flask

from rooms import rooms_routes

app = flask.Flask(__name__)
app.register_blueprint(rooms_routes)


@app.route("/")
def test():
    return "/"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run("0.0.0.0", port)
