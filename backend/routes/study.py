from flask import Blueprint, jsonify, request
from services.cognitive_engine import calculate_cognitive_load
from models import db, StudySession
from datetime import datetime

study_bp = Blueprint("study", __name__)

# Dashboard
@study_bp.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    data = calculate_cognitive_load()
    return jsonify(data)

# Start Session
@study_bp.route("/start-session", methods=["POST"])
def start_session():
    data = request.json

    session = StudySession(
        user_id=data["user_id"]
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({
        "message": "Session started",
        "session_id": session.id
    })

# End Session
@study_bp.route("/end-session", methods=["POST"])
def end_session():
    data = request.json

    session = StudySession.query.get(data["session_id"])

    if session:
        session.end_time = datetime.utcnow()
        session.avg_load = data.get("avg_load", "Optimal")
        db.session.commit()

        return jsonify({"message": "Session ended"})

    return jsonify({"message": "Session not found"}), 404

# Hello Test
@study_bp.route("/hello")
def hello():
    return "Study working"
