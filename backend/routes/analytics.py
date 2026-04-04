from flask import Blueprint, jsonify
from models import StudySession
from werkzeug.security import generate_password_hash, check_password_hash


analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/<int:user_id>")
def analytics(user_id):
    sessions = StudySession.query.filter_by(user_id=user_id).all()

    total_sessions = len(sessions)

    return jsonify({
        "totalSessions": total_sessions,
        "message": "Analytics generated from DB"
    })
