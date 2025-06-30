from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
import json, logging
from os import environ as env
from urllib.parse import quote_plus, urlencode
from datetime import datetime

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
logging.basicConfig(level=logging.INFO)

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = token.get("userinfo")
    app.logger.info(f"LOGIN: user_id={user_info['sub']} email={user_info['email']} at={datetime.now()}")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?" + urlencode({
            "returnTo": url_for("home", _external=True),
            "client_id": env.get("AUTH0_CLIENT_ID")
        }, quote_via=quote_plus)
    )

@app.route("/protected")
def protected():
    if "user" not in session:
        app.logger.warning(f"UNAUTHORIZED access to /protected at={datetime.now()}")
        return redirect("/login")
    user_info = session["user"]["userinfo"]
    app.logger.info(f"ACCESS: /protected by user_id={user_info['sub']} email={user_info['email']} at={datetime.now()}")
    return render_template("protected.html", user=session["user"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))
