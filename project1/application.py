import os, json,  requests
from flask import Flask, session, render_template, redirect, request
from functools import wraps
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from flask import g, request, redirect, url_for

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



#https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

	session.clear()

	username= request.form.get("username")
	try:
		if request.method == "POST":
			rada = db.execute("SELECT * FROM users WHERE username = :username", {"username":username})
			result = rada.fetchone()

			session["user_id"] = result[0]
			session["password"] = result[1]
			return redirect("/")
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
			try:
				db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":request.form.get("username"), "password":hashed})
				db.commit()
				try:
					return redirect("/login")
				except:
					return render_template("/error.html", message="Passwords don't match, try again")
			except:
				return render_template("/error.html", message="This username is already taken")


	else:
		return render_template("/register.html")

@app.route("/logout")
def logout():

	session.clear()

	return redirect("/login")



@app.route("/search", methods=["GET"])
@login_required
def search():

	if not request.args.get("book"):
		return render_template("error.html", message="Please specify what book you want to look for")

	query = "%" + request.args.get("book") + "%"
	query = query.title()

	rada = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :query OR title LIKE :query OR author LIKE :query", {"query":query})

	try:
		books = rada.fetchall()
	except book_not_found:
		return render_template("error.html", message="No such a book was found")
	
	return render_template("query.html", books=books)

@app.route("/book/<isbn>", methods=['GET', 'POST'])
@login_required
def book(isbn):

	rada = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn=:isbn", {"isbn":isbn})
	vysledek = rada.fetchall()

	if vysledek ==0:
		return render_template("error.html", message="Please tell us what book you want to look for")
	else:
		info = rada.fetchall()

	reviews = db.execute("SELECT comment, rating FROM reviews WHERE isbn=:isbn", {"isbn":isbn})
	reviews = reviews.fetchall()

	
	if request.method == "POST":
		currentUser = session["user_id"]
		comment = request.form.get("comment")
		rating = request.form.get("rating")
		
		try:
			db.execute("INSERT INTO reviews (user_id, isbn, comment, rating) VALUES (:user_id, :isbn, :comment, :rating)", {"user_id":currentUser, "isbn": isbn, "comment":comment, "rating":rating})
			db.commit()					
			return render_template("thanks.html")
		except:
			return render_template("error.html", message="You have already submmitted a review!")
	else:
		rada = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn})
		info = rada.fetchall()
		key = os.getenv("GOODREADS_KEY")
		query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
		response = query.json()
		response = response['books'][0]
		info.append(response)
		rada = db.execute("SELECT isbn FROM books WHERE isbn = :isbn", {"isbn": isbn})

		book = rada.fetchone()
		book = book[0]
		results = db.execute("SELECT users.username, comment, rating FROM users INNER JOIN reviews ON users.user_id = reviews.user_id WHERE isbn = :book", {"book": book})

		reviews = results.fetchall()

		return render_template("bookdetail.html", book=book, info=info, reviews=reviews)

@app.route("/api/<isbn>", methods=['GET'])
@login_required
def api_call(isbn):
    rada = db.execute("SELECT title, author, year, isbn, COUNT(reviews.id) as review_count, AVG(reviews.rating) as average_score FROM books INNER JOIN reviews ON books.isbn = reviews.isbn WHERE isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn})
    if rada.rowcount != 1:
        return jsonify("error.html", message="cannot display the results")    
    tmp = rada.fetchone()
    result = dict(tmp.items())
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)	


		



