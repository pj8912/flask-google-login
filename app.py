import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from dotenv import load_dotenv

load_dotenv()

# SQLITE CONFIG
import sqlite3
conn  =  sqlite3.connect('users.sqlite3', check_same_thread=False)
cursor = conn.cursor()




app = Flask("flask-login-app")
app.secret_key = os.environ.get("APP_SECRET") # make sure 

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = os.environ.get("CLIENT_ID")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:3000/callback"
)


flow2 = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:3000/login/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


# @app.route("/login")
# def login():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)


@app.route('/googlelogin')
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    if "google_id" not in session:
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!
       
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        conn  =  sqlite3.connect('users.sqlite3')
        cursor = conn.cursor()
        
        sql = "INSERT INTO users(username, user_email, user_oauth_id, user_oauth_platform) VALUES(?,?,?,?)"
        cursor.execute(sql,(id_info.get("name"),id_info.get("email"),id_info.get("sub"),"google"))
        conn.commit()    

        # session["google_id"] = id_info.get("sub")
        # session["name"] = id_info.get("name")
        # session["email"] = id_info.get("email")

        return redirect("/")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    if "google_id" in session:
        session.clear()
        return redirect("/")
    else :
        return redirect("/")


@app.route("/")
def index():
    if "google_id" in session:
        return render_template('index.html', logged_in=True, username=session['name'])   
    # return "Hello World <a href='/login'><button>Login</button></a>"
    else: 
        return render_template('index.html', logged_in=False)   


# @app.route("/register")
# # @login_is_required #check if logged in 
# def protected_area():
#     # return f"Hello {session['name']} - {session['google_id']}! <br/> <a href='/logout'><button>Logout</button></a>"
#     return redirect('register.html')

@app.route("/register")
def register_page():
    return redirect("/")

@app.route('/signin')
def sign_in():
    return render_template('signin.html')


@app.route('/googlelogin_callback')
def google_login_callback():
    authorization_url, state = flow2.authorization_url()
    session["state2"] = state
    return redirect(authorization_url)

@app.route("/login/callback")
def login_callback():
    if "google_id" in session: 
        return abort(404)
    
    flow2.fetch_token(authorization_response=request.url)

    if not session["state2"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow2.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    conn  =  sqlite3.connect('users.sqlite3')
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE user_oauth_id == ?"
    cursor.execute(sql, (id_info.get("sub"),))
    row = cursor.fetchall()
    if row: 
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        # return render_template('index.html', logged_in=True, username=session['name'])
        return redirect('/')

    else:
        return redirect('/register')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)