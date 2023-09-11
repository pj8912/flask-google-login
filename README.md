# flask-google-login
Register and Login using Google


## Install requirements

```shell
pip install -r requirements.txt
```

> In google developer console create a project and credentials

## Setup `.env` variables
- `APP_SECRET=` YOUR CLIENT SECRET
- `CLIENT_ID=` YOUR CLIENT ID 

## Download Client Secret
- Download your `client secret` json file and rename it to `client_secret.json` and place it in the root folder of this app


## Create SQLite database
- Run `python created_db.py` to create your the sqlite databse `users.sqlite3` which will store the users on registration automatically.


## Add `/callback(s)` URIs to Authorized URIs in google developer console

- The app runs on `http://localhost:3000`
- I use two different routes for login and registration
- In you `Authorized URIs` section add these following two URIs 
   
   - ```
     http://localhost:300/callback
     ```
   - ```
     http://localhost:3000/login/callback
     ```
    
    and click `SAVE`  

## Start
- Start application
    ```
    python app.py
    ```
## Working 

- Seperate flows for registeration and login

- On registration the google's username, password and the oauthId which is unique per user is stored in the database and redirected to home

- On login, the process takes flow and checks the email that is used for login is already in the database and creates a session redirecting to home where you can see a welcome message and logout link, or it will simply redirect to home
