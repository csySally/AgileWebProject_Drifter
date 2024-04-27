from flask import Flask, render_template, request

app = Flask(__name__)

# create SQLite DB connection
conn = sqlite3.connect('testDatabase.db')
cursor = conn.cursor()

# create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS testUser (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT
    )
''')
conn.commit()

app = Flask(__name__)

# route to handle request form root dir
@app.route('/')
def index():
    return 'Hello, World! This is a Flask app.'

if __name__ == '__main__':
    app.run(debug=True)