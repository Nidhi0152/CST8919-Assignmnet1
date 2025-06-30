from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
import json, logging
from os import environ as env
from urllib.parse import quote_plus, urlencode
from datetime import datetime

# Load environment variables
load_dotenv(find_dotenv())

# Initialize Flask app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Configure Auth0 OAuth client
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# Home Route
@app.route("/")
def home():
    try:
        return render_template("home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))
    except Exception as e:
        app.logger.error(f"Error rendering home.html: {e}")
        return "Internal Server Error – Check logs", 500

# Login Route
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

# Callback Route
@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = token.get("userinfo")
    app.logger.info(f"LOGIN: user_id={user_info['sub']} email={user_info['email']} at={datetime.now()}")
    return redirect("/")

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?" + urlencode({
            "returnTo": url_for("home", _external=True),
            "client_id": env.get("AUTH0_CLIENT_ID")
        }, quote_via=quote_plus)
    )

# Protected Route
@app.route("/protected")
def protected():
    if "user" not in session:
        app.logger.warning(f"UNAUTHORIZED access to /protected at={datetime.now()}")
        return redirect("/login")
    try:
        user_info = session["user"]["userinfo"]
        app.logger.info(f"ACCESS: /protected by user_id={user_info['sub']} email={user_info['email']} at={datetime.now()}")
        return render_template("protected.html", user=session["user"])
    except Exception as e:
        app.logger.error(f"Error rendering protected.html: {e}")
        return "Internal Server Error – Check logs", 500

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))
