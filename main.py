import sqlite3
from flask import Flask, render_template, request, redirect

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        created_at TEXT,
        updated_at TEXT
    );
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    image TEXT,
    user_id INTEGER,
    created_at TEXT,
    updated_at TEXT
);
""")

conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * from contacts")
    names = cursor.fetchall()
    conn.close()
    return render_template('index.html', names=names)

@app.route("/create", methods=["POST"])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (name,email,phone) VALUES (?,?,?)', (name, email, phone)
    )

    conn.commit()
    conn.close()
    return redirect('/')

@app.route("/delete/<id>")
def delete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM contacts WHERE id = ?;', (id,)
    )

    conn.commit()
    conn.close()
    return redirect('/')




if __name__ == "__main__":
    app.run()