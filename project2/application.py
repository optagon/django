import os
import time
from functools import wraps
from flask import Flask, render_template, session, request, g, redirect, url_for
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set") 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app.config["SECRET_KEY"] = "my_secret"
socketio = SocketIO(app, async_mode = None)


channels = []
my_messages = {}

#https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():

	session.clear()

	username= request.form.get("username")
	try:
		if request.method == "POST":
			rada = db.execute("SELECT * FROM users WHERE username = :username", {"username":username})
			result = rada.fetchone()

			session["id"] = result[0]
			session["password"] = result[1]
			return redirect("/index")
		else:
			return render_template("login.html")
	except:
		return render_template("/error.html", message="You don't have an account yet")

@app.route("/register", methods=["GET", "POST"])
def register():

	session.clear()

	if request.method == 'POST':
	
		if request.form.get("password") == request.form.get("confirmation"):
			hashed = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
			
			db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":request.form.get("username"), "password":hashed})
			db.commit()
				
		return redirect("/login")


	else:
		return render_template("/register.html")

@app.route("/logout")
def logout():

	session.clear()

	return redirect("/login")


@socketio.on("username")
def receive_username(username):
	users[username] = request.sid

@socketio.on("room_message")
def messageHandler(json):
	my_time = time.ctime(time.time())
	my_data ={"user": json["user"], "msg" : json["msg"], "my_time": my_time}
	my_messages[json["channel"]].append(my_data)
	if len(my_messages[json["channel"]]) > 100:
		my_messages[json["channel"]].pop(0)
	print("Message passed on!")
	emit("room_message", my_data, room = json["channel"])

@socketio.on("channel_creation")
def channel_creation(channel):
	if channel in channels:
		emit("channel_error", "This name is already taken!")
	else:
		channels.append(channel)
		my_messages[channel] = []
		join_room(channel)
		current_channel = channel
		data = {"channel": channel, "messages": my_messages[channel]}
		emit("join_channel", data)

@socketio.on("join_channel")
def join_channel(channel):
	join_room(channel)
	data = {"channel": channel, "messages": my_messages[channel]}
	print(data)
	emit("join_channel", data)

@socketio.on("leave_channel")
def leave_channel(channel):
	leave_room(channel)
	emit("leave_channel", channel)

@socketio.on("change_channel")
def change_channel(old_channel, new_channel):
	leave_room(old_channel)
	join_room(new_channel)
	data = {"channel": new_channel, "messages": my_messages[new_channel]}
	emit("join_channel", data)


@app.route("/index")
@login_required
def index():
	return render_template("index.html", channels = channels, async_mode = socketio.async_mode)


if __name__ == "__main__":
	socketio.run(app, debug = True)
