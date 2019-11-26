import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_URL = "postgres://mmgpuycrhidfhq:bee565f385b5373dd0a0bf12a30a1a878cfeb97aaddd8c5ede9d52160ba6cc94@ec2-54-225-173-42.compute-1.amazonaws.com:5432/d6frcod2mjs1r1"
engine = create_engine(os.getenv(DATABASE_URL))
db = scoped_session(sessionmaker(bind=engine))
reader = csv.reader(open("./books.csv"))

for isbn, title, author, year in reader:
	db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn,  "title": title,"author": author,"year": year})
	db.commit()