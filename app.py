from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

SCOPE = "user-top-read"


@app.route("/")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/redirect")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("wrapped", _external=True))


@app.route("/top")
def wrapped():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info["access_token"])

    track_data = sp.current_user_top_tracks(limit=5, offset=0)["items"]
    tracks_info = [
        {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "cover": track["album"]["images"][0]["url"],
        }
        for track in track_data
    ]

    return render_template("index.html", tracks=tracks_info)


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope=SCOPE,
    )


def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info
