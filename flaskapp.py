from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xe9\xaf\xcd25\xf0\xe6\x1d\x1b\x06q\x19\x05\xa8\x90\x15( \xcd\xca\xb6a\x85\n'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        user = User.query.filter_by(username=username).first()
        if (user.password == password1):
            session['user_id'] = user.id
            return redirect(url_for('user_details'))
        else:
            return render_template('index.html', message='Invalid username or password')
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
       # hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=request.form['username'], 
                        password=request.form['password'],
                        firstname=request.form['firstname'],
                        lastname=request.form['lastname'],
                        email=request.form['email'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/user_details')
def user_details():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return render_template('user_details.html', firstname=user.firstname, lastname=user.lastname, email=user.email)
        else:
            return 'User not found', 404
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)