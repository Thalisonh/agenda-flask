import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

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
    updated_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
""")

conn.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afd56456sad'

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * from contacts WHERE user_id = ?", (session['user_id'],))

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
        'INSERT INTO contacts (name,email,phone, user_id) VALUES (?,?,?,?)', (name, email, phone, session['user_id'])
    )

    conn.commit()
    conn.close()
    flash('Contato criado com sucesso', 'success')
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
    flash('Contato deletado com sucesso', 'success')
    return redirect('/')

@app.route("/update/<id>", methods=['POST'])
def update(id):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?;',(name, email, phone, id)
    )

    conn.commit()
    conn.close()
    flash('Contato alterado com sucesso', 'success')
    return redirect('/')

@app.route("/login", methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ?;',(email,)
    )
    user = cursor.fetchone()
    conn.close()

    print('IF')

    if not user or not check_password_hash(user[3], password):
        flash('Login incorreto!', 'error')
        return redirect('/login')

    session['user_id'] = user[0]
    flash('Bem vindo, ' + user[1], 'success')
    return redirect('/')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?;', (email,))

    user = cursor.fetchone()

    if user:
        conn.close()
        flash('Email já existe', 'error')
        return redirect('/signup')

    cursor.execute('INSERT INTO users (name, email, password) VALUES (?,?,?);', (name, email, generate_password_hash(password, method='sha256')))

    conn.commit()
    conn.close()
    flash('Usuário criado com sucesso', 'success')

    return redirect('/login')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)