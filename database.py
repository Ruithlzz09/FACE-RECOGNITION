#Dependencies
import sqlite3
import os

def create_required(db='database.db'):
	if not os.path.exists('./recognizer'):
	 os.makedirs('./recognizer')
	 print("recognizer folder created")

	if not os.path.exists('./dataset'):
		os.makedirs('./dataset')
		print("dataset folder created")

	conn = sqlite3.connect(db)
	c = conn.cursor()

	sql = """
	DROP TABLE IF EXISTS users;
	CREATE TABLE users (
	           id integer unique primary key autoincrement,
	           name text 
	);
	"""
	c.executescript(sql)
	conn.commit()
	conn.close()
	print()
	return 1

