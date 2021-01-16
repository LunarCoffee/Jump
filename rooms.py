import opentok

import ids
from main import app

OPENTOK_API_KEY = "***REMOVED***"
OPENTOK_API_SECRET = "***REMOVED***"

api_opentok = opentok.OpenTok(OPENTOK_API_KEY, OPENTOK_API_SECRET)

rooms = {}


class Room:
    def __init__(self, session):
        self.session = session


@app.route("/rooms/create")
def rooms_create_get():
    room = Room(api_opentok.create_session())
    room_id = ids.generate()
    rooms[room_id] = room
    return {"room_id": room_id}
    # TODO: establish game parameters


@app.route("/rooms/join/<room_id>")
def rooms_create_get(room_id):
    session = rooms[room_id].session
    token = session.generate_token()
    sid = session.session_id
    return {"session_id": sid, "token": token}
