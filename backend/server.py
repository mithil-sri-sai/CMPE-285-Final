"""
server.py - Swipe-to-vote backend (Flask + SQLite)
Endpoints:
  GET    /items                    - list all items
  POST   /vote                     - record a vote { itemId, choice, sessionId, decisionMs? }
  DELETE /vote                     - remove a vote (undo) { itemId, sessionId }
  GET    /results                  - aggregate yes/no per item
  GET    /session-votes/<id>       - votes for a session (resume)
  POST   /auth/signin              - { sessionId, username }
  GET    /auth/session/<id>        - username for session
  GET    /analytics                - aggregate stats (?sessionId= for personal stats)
"""

import json
import os
import sqlite3
import uuid
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
DB_PATH = os.path.join(BASE_DIR, "votes.db")
PETS_PATH = os.path.join(BASE_DIR, "pets.json")

# --- Load pets from JSON -------------------------------------------------

with open(PETS_PATH) as f:
    PETS = json.load(f)

PETS_BY_ID = {p["id"]: p for p in PETS}

# --- Database helpers ----------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def valid_session_id(session_id: str) -> bool:
    return bool(session_id) and all(
        c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        for c in session_id
    )


def valid_username(username: str) -> bool:
    if not username or len(username) < 2 or len(username) > 24:
        return False
    return all(c.isalnum() or c in "-_" for c in username)


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id          TEXT PRIMARY KEY,
                session_id  TEXT NOT NULL,
                item_id     TEXT NOT NULL,
                choice      TEXT NOT NULL CHECK(choice IN ('yes','no')),
                decision_ms INTEGER,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, item_id)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                session_id  TEXT PRIMARY KEY,
                username    TEXT NOT NULL UNIQUE,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        try:
            db.execute("ALTER TABLE votes ADD COLUMN decision_ms INTEGER")
        except sqlite3.OperationalError:
            pass
        db.commit()

# --- Routes --------------------------------------------------------------

@app.route("/")
def serve_app():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(PETS)


@app.route("/vote", methods=["POST"])
def record_vote():
    data = request.get_json(silent=True) or {}
    item_id   = str(data.get("itemId", "")).strip()
    choice    = str(data.get("choice", "")).strip().lower()
    session_id = str(data.get("sessionId", "")).strip()

    # Validate
    if not item_id or item_id not in PETS_BY_ID:
        return jsonify({"error": "invalid itemId"}), 400
    if choice not in ("yes", "no"):
        return jsonify({"error": "choice must be 'yes' or 'no'"}), 400
    if not valid_session_id(session_id):
        return jsonify({"error": "invalid sessionId"}), 400

    decision_ms = data.get("decisionMs")
    if decision_ms is not None:
        try:
            decision_ms = int(decision_ms)
            if decision_ms < 0 or decision_ms > 300000:
                decision_ms = None
        except (TypeError, ValueError):
            decision_ms = None

    db = get_db()
    try:
        vote_id = str(uuid.uuid4())
        db.execute(
            "INSERT INTO votes (id, session_id, item_id, choice, decision_ms) VALUES (?, ?, ?, ?, ?)",
            (vote_id, session_id, item_id, choice, decision_ms),
        )
        db.commit()
        return jsonify({"status": "ok", "voteId": vote_id}), 201
    except sqlite3.IntegrityError:
        # Duplicate — update the existing vote (undo/redo semantics)
        db.execute(
            "UPDATE votes SET choice = ?, decision_ms = ? WHERE session_id = ? AND item_id = ?",
            (choice, decision_ms, session_id, item_id),
        )
        db.commit()
        return jsonify({"status": "updated"}), 200


@app.route("/results", methods=["GET"])
def get_results():
    db = get_db()
    rows = db.execute("""
        SELECT item_id,
               SUM(CASE WHEN choice='yes' THEN 1 ELSE 0 END) AS yes_count,
               SUM(CASE WHEN choice='no'  THEN 1 ELSE 0 END) AS no_count,
               COUNT(*) AS total
        FROM votes
        GROUP BY item_id
    """).fetchall()

    result_map = {r["item_id"]: dict(r) for r in rows}

    results = []
    for pet in PETS:
        agg = result_map.get(pet["id"], {"yes_count": 0, "no_count": 0, "total": 0})
        yes = agg["yes_count"]
        no  = agg["no_count"]
        total = yes + no
        yes_pct = round(yes / total * 100) if total else 0
        results.append({
            **pet,
            "yes": yes,
            "no":  no,
            "total": total,
            "yes_pct": yes_pct,
            "divisiveness": abs(50 - yes_pct),  # 0 = perfectly divisive
        })

    return jsonify(results)


@app.route("/vote", methods=["DELETE"])
def delete_vote():
    """Remove a vote (undo last swipe)."""
    data = request.get_json(silent=True) or {}
    item_id = str(data.get("itemId", "")).strip()
    session_id = str(data.get("sessionId", "")).strip()

    if not item_id or item_id not in PETS_BY_ID:
        return jsonify({"error": "invalid itemId"}), 400
    if not valid_session_id(session_id):
        return jsonify({"error": "invalid sessionId"}), 400

    db = get_db()
    cur = db.execute(
        "DELETE FROM votes WHERE session_id = ? AND item_id = ?",
        (session_id, item_id),
    )
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "vote not found"}), 404
    return jsonify({"status": "deleted"})


@app.route("/session-votes/<session_id>", methods=["GET"])
def session_votes(session_id):
    """Return all votes cast in this session (for undo/resume)."""
    if not valid_session_id(session_id):
        return jsonify({"error": "invalid sessionId"}), 400
    db = get_db()
    rows = db.execute(
        "SELECT item_id, choice FROM votes WHERE session_id = ?", (session_id,)
    ).fetchall()
    return jsonify({r["item_id"]: r["choice"] for r in rows})


@app.route("/auth/signin", methods=["POST"])
def auth_signin():
    data = request.get_json(silent=True) or {}
    session_id = str(data.get("sessionId", "")).strip()
    username = str(data.get("username", "")).strip()

    if not valid_session_id(session_id):
        return jsonify({"error": "invalid sessionId"}), 400
    if not valid_username(username):
        return jsonify({"error": "username must be 2–24 letters, numbers, - or _"}), 400

    db = get_db()
    taken = db.execute(
        "SELECT session_id FROM users WHERE username = ? AND session_id != ?",
        (username, session_id),
    ).fetchone()
    if taken:
        return jsonify({"error": "username already taken"}), 409

    db.execute(
        """
        INSERT INTO users (session_id, username, last_seen)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            username = excluded.username,
            last_seen = CURRENT_TIMESTAMP
        """,
        (session_id, username),
    )
    db.commit()
    return jsonify({"status": "ok", "username": username})


@app.route("/auth/session/<session_id>", methods=["GET"])
def auth_session(session_id):
    if not valid_session_id(session_id):
        return jsonify({"error": "invalid sessionId"}), 400
    db = get_db()
    row = db.execute(
        "SELECT username FROM users WHERE session_id = ?", (session_id,)
    ).fetchone()
    if not row:
        return jsonify({"username": None})
    return jsonify({"username": row["username"]})


@app.route("/analytics", methods=["GET"])
def analytics():
    db = get_db()
    session_id = request.args.get("sessionId", "").strip()

    total_swipes = db.execute("SELECT COUNT(*) AS n FROM votes").fetchone()["n"]
    total_sessions = db.execute(
        "SELECT COUNT(DISTINCT session_id) AS n FROM votes"
    ).fetchone()["n"]
    signed_in_users = db.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    yes_count = db.execute(
        "SELECT COUNT(*) AS n FROM votes WHERE choice = 'yes'"
    ).fetchone()["n"]
    no_count = db.execute(
        "SELECT COUNT(*) AS n FROM votes WHERE choice = 'no'"
    ).fetchone()["n"]
    avg_row = db.execute(
        "SELECT AVG(decision_ms) AS avg_ms FROM votes WHERE decision_ms IS NOT NULL"
    ).fetchone()
    avg_decision_ms = round(avg_row["avg_ms"]) if avg_row["avg_ms"] is not None else None

    payload = {
        "totalSwipes": total_swipes,
        "totalSessions": total_sessions,
        "signedInUsers": signed_in_users,
        "yesCount": yes_count,
        "noCount": no_count,
        "avgDecisionMs": avg_decision_ms,
        "you": None,
    }

    if valid_session_id(session_id):
        you_votes = db.execute(
            "SELECT COUNT(*) AS n FROM votes WHERE session_id = ?", (session_id,)
        ).fetchone()["n"]
        you_yes = db.execute(
            "SELECT COUNT(*) AS n FROM votes WHERE session_id = ? AND choice = 'yes'",
            (session_id,),
        ).fetchone()["n"]
        you_avg = db.execute(
            "SELECT AVG(decision_ms) AS avg_ms FROM votes WHERE session_id = ? AND decision_ms IS NOT NULL",
            (session_id,),
        ).fetchone()["avg_ms"]
        user_row = db.execute(
            "SELECT username FROM users WHERE session_id = ?", (session_id,)
        ).fetchone()
        payload["you"] = {
            "username": user_row["username"] if user_row else None,
            "votes": you_votes,
            "yesCount": you_yes,
            "noCount": you_votes - you_yes,
            "avgDecisionMs": round(you_avg) if you_avg is not None else None,
        }

    return jsonify(payload)


if __name__ == "__main__":
    init_db()
    print("✅ Database initialised")
    print("🚀 Starting server on http://localhost:5050")
    app.run(host="0.0.0.0", port=5050, debug=False)
