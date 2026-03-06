from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os, random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
app.secret_key = "moodyfication_secret_key"

sp = None
try:
    auth = SpotifyClientCredentials(
        client_id="Null(Add_Here)",
        client_secret="Null(Add_Here)",
    )
    sp = spotipy.Spotify(auth_manager=auth)
except:
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moodyfication.db")

QUOTES = [
    "Music is the universal language of mankind.<br>- Henry Wadsworth Longfellow",
    "Where words fail, music speaks.<br>- Hans Christian Andersen",
    "Music gives a soul to the universe.<br>- Plato",
    "Good thing about music? When it hits, you feel no pain.<br>- Bob Marley",
    "Music is the soundtrack of your life.<br>- Dick Clark",
    "Without music, life would be a mistake.<br>- Friedrich Nietzsche",
    "Music expresses that which cannot be said.<br>- Victor Hugo",
    "Life is like a beautiful melody, only the lyrics are messed up.<br>- Hans Christian Andersen",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_greeting():
    h = datetime.now().hour
    if h < 12:
        return "Good Morning"
    elif h < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"


def get_current_mood():
    if "current_mood_id" not in session:
        return None
    conn = get_db()
    mood = conn.execute(
        "SELECT * FROM mood WHERE id = ?", (session["current_mood_id"],)
    ).fetchone()
    conn.close()
    return mood


@app.errorhandler(404)
def not_found(e):
    return (
        render_template("error.html", error_code=404, error_message="Page not found."),
        404,
    )


@app.errorhandler(500)
def server_error(e):
    return (
        render_template(
            "error.html", error_code=500, error_message="Something went wrong."
        ),
        500,
    )


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    conn = get_db()
    moods = conn.execute("SELECT * FROM mood WHERE is_custom = 0").fetchall()
    conn.close()
    return render_template("index.html", moods=moods, quote=random.choice(QUOTES))


@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    mood_id = request.form.get("mood_id")
    if not username or not password:
        return redirect(url_for("index"))

    conn = get_db()
    user = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
    if user:
        if not check_password_hash(user["password"], password):
            conn.close()
            return redirect(url_for("index"))
    else:
        conn.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["current_mood_id"] = int(mood_id) if mood_id else 1
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/exit")
def exit_session():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    conn = get_db()
    mood_id = session.get("current_mood_id", 1)
    moods = conn.execute(
        "SELECT * FROM mood WHERE is_custom = 0 OR added_by_user_id = ? ORDER BY is_custom, id",
        (session["user_id"],),
    ).fetchall()
    current_mood = conn.execute(
        "SELECT * FROM mood WHERE id = ?", (mood_id,)
    ).fetchone()
    if not current_mood:
        mood_id = 1
        session["current_mood_id"] = 1
        current_mood = conn.execute("SELECT * FROM mood WHERE id = 1").fetchone()
    playlists = conn.execute(
        "SELECT p.*, u.username as added_by FROM playlist p LEFT JOIN user u ON p.added_by_user_id = u.id WHERE p.mood_id = ? AND (p.added_by_user_id IS NULL OR p.added_by_user_id = ?)",
        (mood_id, session["user_id"]),
    ).fetchall()
    conn.close()
    return render_template(
        "dashboard.html",
        moods=moods,
        current_mood=current_mood,
        playlists=playlists,
        greeting=get_greeting(),
        username=session["username"],
        current_playlist_url=session.get("current_playlist_url", ""),
    )


@app.route("/select_mood/<int:mood_id>")
def select_mood(mood_id):
    session["current_mood_id"] = mood_id
    return redirect(url_for("dashboard"))


@app.route("/play/<int:playlist_id>")
def play_playlist(playlist_id):
    conn = get_db()
    p = conn.execute("SELECT * FROM playlist WHERE id = ?", (playlist_id,)).fetchone()
    if p:
        conn.execute(
            "INSERT INTO activity_log (user_id, mood_id) VALUES (?, ?)",
            (session["user_id"], p["mood_id"]),
        )
        conn.commit()
        session["current_playlist_url"] = p["embed_url"]
        session["current_mood_id"] = p["mood_id"]
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/add_mood", methods=["POST"])
def add_mood():
    name = request.form.get("mood_name", "").strip()
    emoji = request.form.get("mood_emoji", "").strip()
    if name and emoji:
        conn = get_db()
        conn.execute(
            "INSERT INTO mood (name, emoji, css_class, is_custom, added_by_user_id) VALUES (?, ?, 'bg-custom', 1, ?)",
            (name, emoji, session["user_id"]),
        )
        conn.commit()
        new = conn.execute(
            "SELECT id FROM mood WHERE name = ? AND added_by_user_id = ?",
            (name, session["user_id"]),
        ).fetchone()
        conn.close()
        if new:
            session["current_mood_id"] = new["id"]
    return redirect(url_for("dashboard"))


@app.route("/edit_mood/<int:mood_id>", methods=["POST"])
def edit_mood(mood_id):
    name = request.form.get("mood_name", "").strip()
    emoji = request.form.get("mood_emoji", "").strip()
    if name and emoji:
        conn = get_db()
        conn.execute(
            "UPDATE mood SET name = ?, emoji = ? WHERE id = ? AND added_by_user_id = ?",
            (name, emoji, mood_id, session["user_id"]),
        )
        conn.commit()
        conn.close()
    return redirect(url_for("dashboard"))


@app.route("/delete_mood/<int:mood_id>")
def delete_mood(mood_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM mood WHERE id = ? AND is_custom = 1 AND added_by_user_id = ?",
        (mood_id, session["user_id"]),
    )
    conn.execute(
        "DELETE FROM playlist WHERE mood_id = ? AND added_by_user_id = ?",
        (mood_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    session["current_mood_id"] = 1
    return redirect(url_for("dashboard"))


@app.route("/add_spotify_playlist", methods=["POST"])
def add_spotify_playlist():
    pid = request.form.get("playlist_id")
    name = request.form.get("name")
    mid = request.form.get("mood_id")
    if pid and mid:
        conn = get_db()
        conn.execute(
            "INSERT INTO playlist (mood_id, name, embed_url, added_by_user_id) VALUES (?, ?, ?, ?)",
            (
                mid,
                name,
                f"https://open.spotify.com/embed/playlist/{pid}",
                session["user_id"],
            ),
        )
        conn.commit()
        conn.close()
        session["current_mood_id"] = int(mid)
    return redirect(url_for("dashboard"))


@app.route("/delete_playlist/<int:playlist_id>")
def delete_playlist(playlist_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM playlist WHERE id = ? AND added_by_user_id = ?",
        (playlist_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/discover", methods=["GET", "POST"])
def discover():
    if "user_id" not in session:
        return redirect(url_for("index"))
    results = []
    if request.method == "POST" and sp:
        try:
            search = sp.search(
                q=request.form.get("query", ""), type="playlist", limit=10
            )
            for item in search["playlists"]["items"]:
                if item:
                    results.append(
                        {
                            "name": item["name"],
                            "id": item["id"],
                            "image": item["images"][0]["url"] if item["images"] else "",
                            "owner": item["owner"]["display_name"],
                        }
                    )
        except:
            pass
    conn = get_db()
    moods = conn.execute(
        "SELECT * FROM mood WHERE is_custom = 0 OR added_by_user_id = ?",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template(
        "discover.html", results=results, moods=moods, current_mood=get_current_mood()
    )


@app.route("/tracking")
def tracking():
    if "user_id" not in session:
        return redirect(url_for("index"))
    conn = get_db()
    stats = conn.execute(
        "SELECT m.name, m.emoji, m.css_class, COUNT(a.id) as count FROM mood m LEFT JOIN activity_log a ON m.id = a.mood_id AND a.user_id = ? GROUP BY m.id ORDER BY count DESC",
        (session["user_id"],),
    ).fetchall()
    total = sum(s["count"] for s in stats)
    history = conn.execute(
        "SELECT DATE(a.timestamp) as date, TIME(a.timestamp) as time, m.name, m.emoji FROM activity_log a JOIN mood m ON a.mood_id = m.id WHERE a.user_id = ? ORDER BY a.timestamp DESC LIMIT 50",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    processed = [
        {
            "name": s["name"],
            "emoji": s["emoji"],
            "css_class": s["css_class"],
            "count": s["count"],
            "pct": round(s["count"] / total * 100, 1) if total > 0 else 0,
        }
        for s in stats
    ]
    return render_template(
        "tracking.html",
        stats=processed,
        history=history,
        total=total,
        current_mood=get_current_mood(),
    )


@app.route("/clear_history")
def clear_history():
    if "user_id" not in session:
        return redirect(url_for("index"))
    conn = get_db()
    conn.execute("DELETE FROM activity_log WHERE user_id = ?", (session["user_id"],))
    conn.commit()
    conn.close()
    return redirect(url_for("tracking"))


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from setup import init_db

        init_db()
    app.run(debug=True, port=5000)
