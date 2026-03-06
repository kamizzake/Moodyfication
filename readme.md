# 🎵 MoodyFication

> **Music That Matches Your Mood**  
> A mood-driven music web app built on Flask and Spotify API<br>Pick How You feel, Get A Playlist And Start Listening

&nbsp;

Built as part of the **DS3 Web Engineering** Module <br> **XU Exponential University of Applied Sciences** by <br> **Mueed Baloch** and **Diya Pandya** — Winter 2025

---

## The Idea

Most music apps ask you _what_ you want to listen to. We thought a better question is _how are you feeling?_

MoodyFication connects your current mood to curated Spotify playlists, plays them directly in the browser, and quietly keeps track of your listening habits over time. The goal was to build something genuinely useful and simple enough for anyone to pick up.

---

## What It Does

- **Mood Selection** —> choose from 6 built-in moods, each with its own color theme and playlist collection. Not feeling any of them? Create your own custom mood.
- **Embedded Player** —> Spotify playlists play right inside the app. No new tabs, no redirects.
- **Discover** —> search Spotify directly from the app and save any playlist you find to whichever mood fits it best.
- **Mood Tracking** —> every time you play something, it gets logged. Over time you get a visual breakdown of your listening habits via distribution bars, a history table, your top mood.
- **Sessions** —> login with a username and PIN. No email, no registration form, no fuss.
- **Dynamic Themes** —> entire apps background gradient shifts based on whichever mood is currently selected.

---

## Tech Stack

### Backend

| Technology | Purpose                                            |
| ---------- | -------------------------------------------------- |
| Python     | Core Language                                      |
| Flask      | Web Framework and Routing                          |
| SQLite     | Database —> users, moods, playlists, activity logs |
| Spotipy    | Python wrapper for the Spotify Web API             |
| Werkzeug   | Password hashing for session security              |

### Frontend

| Technology     | Purpose                             |
| -------------- | ----------------------------------- |
| HTML5 / CSS3   | Structure and Styling               |
| JavaScript     | Modal interactions via `main.js`    |
| Bootstrap 5    | UI components and responsive layout |
| Font Awesome 6 | Icons throughout the interface      |

### Infrastructure

| Tool           | Purpose                                                    |
| -------------- | ---------------------------------------------------------- |
| PythonAnywhere | Hosting and Deployment                                     |
| GitHub Repos   | Version control and collaboration                          |
| VS Code        | Primary Editor with formatting and productivity extensions |

---

## Project Structure

```
MoodyFication/
│
├── static/
│   ├── style.css        # All custom styles, mood themes, layout
│   ├── main.js          # Modal open/close logic
│   └── icon.jpg         # App icon
│
├── templates/
│   ├── base.html        # Shared layout — sidebar, player, nav
│   ├── index.html       # Landing and login page
│   ├── dashboard.html   # Main player and mood selection
│   ├── tracking.html    # Stats, distribution, history log
│   ├── discover.html    # Spotify search and playlist saving
│   └── error.html       # 404 and 500 error pages
│
├── app.py               # All Flask routes and business logic
├── setup.py             # Database creation and seed data
└── require.txt          # Python dependencies
```

---

## Database Design

Four Tables, Kept Simple:

```
user           — id, username, password (hashed)
mood           — id, name, emoji, css_class, is_custom, added_by_user_id
playlist       — id, mood_id, name, embed_url, added_by_user_id
activity_log   — id, user_id, mood_id, timestamp
```

The `activity_log` table is what powers the tracking page —> every time a user plays a playlist, a row is inserted with their user ID, the mood ID, and a timestamp. The tracking page then aggregates this with a `GROUP BY` query to produce the stats and distribution.

---

## Functional Requirements

These are the core things the app does:

- Users can register and log in using a username and PIN
- Users can select a mood from a list of built-in options
- Users can create, edit, and delete their own custom moods
- Users can browse and play playlists associated with current mood
- Users can view their mood distribution stats and full history log
- Users can search Spotify for playlists and add them to any mood
- The app logs every playlist play to user's activity history
- Users can delete playlists they added
- Users can clear their history
- The app handles 404 and 500 errors

## Non-Functional Requirements

- **Usability** —> three column layout with persistent player, no page jumping or loss of context
- **Performance** —> lightweight stack, no heavy frameworks on the frontend, minimal JS
- **Simplicity** —> session login takes under 30 seconds, the interface is self explanatory
- **Portability** —> runs locally with three commands, deployable to PythonAnywhere without changes

---

## Quick Setup

**1. Clone The Repo**

```bash
git clone https://github.com/YOUR_USERNAME/MoodyFication.git
cd MoodyFication
```

**2. Install Dependencies**

```bash
pip install -r require.txt
```

**3. Initialize Database**  
This creates all tables and seeds the 6 default moods and 24 playlists:

```bash
python setup.py
```

**4. Run The App**

```bash
python app.py
```

**5. Open In Browser**

```
http://127.0.0.1:5000
```

> **Note:** For the embedded Spotify player and Discover feature to work properly, make sure you are logged into your Spotify account in the same browser session. A Spotify Premium account gives the best experience.

---

## Spotify API

MoodyFication uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api) via the [Spotipy](https://spotipy.readthedocs.io/) Python library. The API is used for:

- **Searching playlists** on the Discover page via `sp.search()`
- **Embedding playlists** via Spotify's embed URL format

Authentication uses the **Client Credentials** flow —> no user OAuth required, which keeps the setup simple. The client ID and secret are stored directly in `app.py`.

---

## Deployment

MoodyFication is deployed on **PythonAnywhere** —> a Python-friendly hosting platform that supports Flask apps with minimal configuration.

Updates follow this flow:

1. Changes are committed and pushed to GitHub/Bitbucket
2. The PythonAnywhere console pulls the latest version via `git pull`
3. The web app is reloaded from the PythonAnywhere dashboard

No Build Step, No Pipeline — Just Pull and Reload

---

## Known Limitations

- Spotify embed player requires an active Spotify session in browser to play full tracks
- SQLite is sufficient for a small deployment but would need replacing at scale
- No OAuth login means the app cannot access private user Spotify data
- Designed for desktop use, no mobile optimized layout currently

---

## 🛠️ Built With

- [Flask](https://flask.palletsprojects.com/) — Python Web Framework
- [Spotipy](https://spotipy.readthedocs.io/) — Spotify Web API Wrapper
- [Bootstrap 5](https://getbootstrap.com/) — UI Framework
- [SQLite](https://www.sqlite.org/) — Lightweight Database

---

_MoodyFication — Made For Music lovers_ 🎧
_Work In Progress_
