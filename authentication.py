from flask import Flask , render_template , request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key ="secrt123" #needed for session



# create database table
def create_table():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template('home.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO users(username, password) VALUES (?, ?)",
                     (username, password))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("register.html")


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/welcome')

        else:
            return "Invalid username"

    return render_template("login.html")

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


# logout

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
