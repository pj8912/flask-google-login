@app.route("/callback")
def callback():
   if "google_id" in session:
      return redirect("/")
     
   flow.fetch_token(authorization_reponse=request.url)
   if not session["state"] == request.args["state"]:abort(500)
     
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

    sql = "SELECT * FROM users WHERE user_oauth_id == ?"
    cursor.execute(sql, (id_info.get("sub"),))
    row = cursor.fetchall()
    #login
    if row:
    	session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        # return render_template('index.html', logged_in=True, username=session['name'])
        return redirect('/')
    else:
        #register user
        sql = "INSERT INTO users(username, user_email, user_oauth_id, user_oauth_platform) VALUES(?,?,?,?)"
        cursor.execute(sql,(id_info.get("name"),id_info.get("email"),id_info.get("sub"),"google"))
        conn.commit()
        
    
