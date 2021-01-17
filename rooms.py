import random
import time

import flask
import opentok
from flask import request

import ids

rooms_routes = flask.Blueprint("rooms_routes", __name__)

OPENTOK_API_KEY = "***REMOVED***"  # lol
OPENTOK_API_SECRET = "***REMOVED***"  # lol

api_opentok = opentok.OpenTok(OPENTOK_API_KEY, OPENTOK_API_SECRET)

EXERCISES = {
    "quick": [[4, "squats"], [8, "jumping jacks"]],
    "core": [[30, "sit-ups"], [1, "plank"], [2, "side planks"]],
    "lower body": [[10, "squats"], [20, "lunges"], [30, "calf raises"], [20, "side lunges"]]
}

rooms = {}


class Room:
    def __init__(self, session, exercises, initiator_id):
        self.session = session
        self.exercises = exercises
        self.initiator_id = initiator_id
        self.archive = None

        self.initiator_score = 0
        self.opponent_score = 0
        self.win_score = len(exercises)


@rooms_routes.route("/rooms/create", methods=["POST"])
def rooms_create_post():
    data = request.get_json(force=True)
    initiator_id = data["user_id"]
    exercises = EXERCISES.get(data["workout"].strip(), "null lunge")

    session = api_opentok.create_session(media_mode=opentok.MediaModes.routed)
    token = session.generate_token(data=f"user={initiator_id}")

    room = Room(session, exercises, initiator_id)
    room_id = ids.generate()
    rooms[room_id] = room

    return {"room_id": room_id,
            "session_id": session.session_id,
            "token": token,
            "exercises": exercises}


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


@rooms_routes.route("/rooms/update", methods=["POST"])
def rooms_update_post():
    data = request.get_json(force=True)
    room_id = data["room_id"]
    user_id = data["user_id"]

    room = rooms[room_id]
    if user_id == room.initiator_id:
        room.initiator_score += 1
    else:
        room.opponent_score += 1

    if room.initiator_score == room.win_score:
        end_data = {"game_over": True, "winner_id": room.initiator_id}
    elif room.opponent_score == room.win_score:
        end_data = {"game_over": True, "winner_id": room.opponent_id}
    else:
        end_data = {"game_over": False, "winner_id": user_id}

    payload = {"data": end_data}
    api_opentok.signal(room.session.session_id, payload)
    return "", 204


@rooms_routes.route("/archives")
def archives_get():
    archives = api_opentok.list_archives()
    return flask.jsonify([a.url for a in archives])


@rooms_routes.route("/archives/<user_id>")
def archives_user_id_get(user_id):
    def is_for_user(name):
        return user_id in name.split("-").split("_")[:2]

    archives = api_opentok.list_archives()
    user_archives = [a.url for a in archives if is_for_user(a.name)]
    return flask.jsonify(user_archives)
