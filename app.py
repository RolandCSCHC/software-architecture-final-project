from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Change this to a secure random key

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "your-google-client-id")
GOOGLE_CLIENT_SECRET = os.environ.get(
    "GOOGLE_CLIENT_SECRET", "your-google-client-secret"
)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

# Disable HTTPS requirement for local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Simple user class for demonstration
class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic


# In-memory user storage (use database in production)
users = {}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route("/")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")



@app.route("/login")
def login():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5001/callback"],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    flow.redirect_uri = url_for("callback", _external=True)

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    # Verify state parameter
    if request.args.get("state") != session.get("state"):
        return "Invalid state parameter", 400

    # Create flow instance
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5001/callback"],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    flow.redirect_uri = url_for("callback", _external=True)

    # Fetch token
    flow.fetch_token(authorization_response=request.url)

    # Get user info from Google
    credentials = flow.credentials
    request_session = google_requests.Request()

    # Verify and decode the JWT token
    idinfo = id_token.verify_oauth2_token(
        credentials.id_token, request_session, GOOGLE_CLIENT_ID
    )

    # Create user object
    user_id = idinfo["sub"]
    user_email = idinfo["email"]
    user_name = idinfo["name"]
    user_picture = idinfo.get("picture", "")

    # Store user in memory (use database in production)
    user = User(user_id, user_name, user_email, user_picture)
    users[user_id] = user

    # Log in the user
    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile", user=current_user)


@app.route("/api/data")
@login_required
def api_data():
    # Example API endpoint - now requires authentication
    data = {
        "message": f"Hello {current_user.name} from Flask API!",
        "status": "success",
        "user_email": current_user.email,
        "data": [1, 2, 3, 4, 5],
    }
    return jsonify(data)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
