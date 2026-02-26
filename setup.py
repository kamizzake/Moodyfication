import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moodyfication.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS mood (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, emoji TEXT NOT NULL, css_class TEXT NOT NULL, is_custom INTEGER DEFAULT 0, added_by_user_id INTEGER)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY AUTOINCREMENT, mood_id INTEGER NOT NULL, name TEXT NOT NULL, embed_url TEXT NOT NULL, added_by_user_id INTEGER, FOREIGN KEY (mood_id) REFERENCES mood(id))"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS activity_log (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, mood_id INTEGER NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()


def seed_data():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM mood").fetchone()[0] != 0:
        conn.close()
        return

    moods = [
        ("Chill", "🌿", "bg-chill", 0),
        ("Energetic", "⚡", "bg-energetic", 0),
        ("Focused", "🧠", "bg-focus", 0),
        ("Happy", "😊", "bg-happy", 0),
        ("Romantic", "❤️", "bg-romantic", 0),
        ("Gloomy", "😢", "bg-gloomy", 0),
    ]
    conn.executemany(
        "INSERT INTO mood (name, emoji, css_class, is_custom) VALUES (?, ?, ?, ?)",
        moods,
    )
    conn.commit()

    m = {
        r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM mood").fetchall()
    }

    playlists = [
        (
            m["Chill"],
            "Chill Vibes",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX889U0CL85jj",
        ),
        (
            m["Chill"],
            "Lo-Fi Beats",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWWQRwui0ExPn",
        ),
        (
            m["Chill"],
            "Peaceful Piano",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO",
        ),
        (
            m["Chill"],
            "Chillout Lounge",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWTvNyxOwkztu",
        ),
        (
            m["Energetic"],
            "Beast Mode",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP",
        ),
        (
            m["Energetic"],
            "Workout Hits",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX70RN3TfWWJh",
        ),
        (
            m["Energetic"],
            "Power Workout",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWUVpAXiEPK8P",
        ),
        (
            m["Energetic"],
            "Adrenaline Rush",
            "https://open.spotify.com/embed/playlist/3k1FLPzgsoGsUHvhvfuPBk",
        ),
        (
            m["Focused"],
            "Deep Focus",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ",
        ),
        (
            m["Focused"],
            "Brain Food",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWXLeA8Omikj7",
        ),
        (
            m["Focused"],
            "Coding Mode",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX5trt9i14X7j",
        ),
        (
            m["Focused"],
            "Study Session",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX8Uebhn9wzrS",
        ),
        (
            m["Happy"],
            "Happy Hits",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
        ),
        (
            m["Happy"],
            "Good Vibes",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWYBO1MoTDhZI",
        ),
        (
            m["Happy"],
            "Feel Good Pop",
            "https://open.spotify.com/embed/playlist/7INcD4lmarWTQiDVodjVt4",
        ),
        (
            m["Happy"],
            "Mood Booster",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
        ),
        (
            m["Romantic"],
            "Love Songs",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M",
        ),
        (
            m["Romantic"],
            "Romantic Evening",
            "https://open.spotify.com/embed/playlist/3a06DTYRmFcgjvWfhEgvSy",
        ),
        (
            m["Romantic"],
            "Date Night",
            "https://open.spotify.com/embed/playlist/3Wak7IlnaUO13U3J2jePEK",
        ),
        (
            m["Romantic"],
            "Love Ballads",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWYMvTygsLWlG",
        ),
        (
            m["Gloomy"],
            "Sad Songs",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
        ),
        (
            m["Gloomy"],
            "Life Sucks",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX3YSRoSdA634",
        ),
        (
            m["Gloomy"],
            "Melancholy",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DX64Y3du11rR1",
        ),
        (
            m["Gloomy"],
            "Rainy Day",
            "https://open.spotify.com/embed/playlist/37i9dQZF1DWV7EzJMK2FUI",
        ),
    ]
    conn.executemany(
        "INSERT INTO playlist (mood_id, name, embed_url) VALUES (?, ?, ?)", playlists
    )
    conn.commit()
    conn.close()


def init_db():
    create_tables()
    seed_data()
    print("Database Ready")


if __name__ == "__main__":
    init_db()
