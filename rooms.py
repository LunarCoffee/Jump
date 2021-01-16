import random
import time

import flask
import opentok
from flask import request

import ids

rooms_routes = flask.Blueprint("rooms_routes", __name__)

OPENTOK_API_KEY = open("opentok_key").read()
OPENTOK_API_SECRET = open("opentok_secret").read()

print(OPENTOK_API_KEY, OPENTOK_API_SECRET)

api_opentok = opentok.OpenTok(OPENTOK_API_KEY, OPENTOK_API_SECRET)

EXERCISES = "squats,pushups,lunges,crunches".split(",")
rooms = {}

class Room:
    def __init__(self, session, exercises, initiator_id):
        self.session = session
        self.exercises = exercises
        self.initiator_id = initiator_id
        self.archive = None


@rooms_routes.route("/rooms/create", methods=["POST"])
def rooms_create_post():
    data = request.get_json(force=True)
    initiator_id = data["user_id"]

    session = api_opentok.create_session(media_mode=opentok.MediaModes.routed, archive_mode=opentok.ArchiveModes.manual)
    exercises = random.sample(EXERCISES, k=len(EXERCISES))

    room = Room(session, exercises, initiator_id)
    room_id = ids.generate()
    rooms[room_id] = room

    return {"room_id": room_id, "exercises": exercises}


@rooms_routes.route("/rooms/join", methods=["POST"])
def rooms_join_post():
    data = request.get_json(force=True)
    room_id = data["room_id"]
    user_id = data["user_id"]

    room = rooms[room_id]
    session = room.session
    token = session.generate_token(data=f"user={user_id}")
    sid = session.session_id

    archive_name = f"{room.initiator_id}-{user_id}_{time.time_ns()}"
    archive = api_opentok.start_archive(session.session_id, name=archive_name)
    rooms[room_id].archive = archive

    return {"session_id": sid, "token": token}
