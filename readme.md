# 🎵 MoodyFication

> Music that matches your mood.

MoodyFication is a mood-based music web app built with Flask and Spotify.  
Pick how you're feeling, get a matching playlist, and start listening — right in the browser.

---

## ✨ Features

- 🎭 **Mood Selection** — Choose from built-in moods or create your own
- 🎵 **Spotify Playlists** — Each mood has curated playlists that play embedded in the app
- 🔍 **Discover** — Search Spotify for playlists and add them to any mood
- 📊 **Mood Tracking** — See your listening history and top moods over time
- 👤 **Sessions** — Simple username + PIN login, no account needed

---

## 🚀 Quick Setup

**1. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/MoodyFication.git
cd MoodyFication
```

**2. Install requirements**

```bash
pip install -r require.txt
```

**3. Set up the database**

```bash
python setup.py
```

**4. Run the app**

```bash
python app.py
```

**5. Open in your browser**

```
http://127.0.0.1:5000
```

> 💡 For the player and Discover feature to work, make sure you're logged into Spotify in the same browser.

---

## 🗂️ Project Structure

```
MoodyFication/
├── static/
│   ├── style.css       # All styles
│   ├── main.js         # Modal helpers
│   └── icon.jpg        # App icon
├── templates/
│   ├── base.html       # Shared layout
│   ├── index.html      # Login / landing page
│   ├── dashboard.html  # Main player page
│   ├── tracking.html   # Mood history & stats
│   ├── discover.html   # Spotify search
│   └── error.html      # Error page
├── app.py              # Flask app & routes
├── setup.py            # Database setup & seeding
└── require.txt         # Dependencies
```

---

## 🛠️ Built With

- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Spotipy](https://spotipy.readthedocs.io/) — Spotify Web API wrapper
- [Bootstrap 5](https://getbootstrap.com/) — UI framework
- [SQLite](https://www.sqlite.org/) — Lightweight database

---

_Work In Progress_
