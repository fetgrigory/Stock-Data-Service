'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 13/07/2025
Ending //

'''
# Installing the necessary libraries
from flask import Flask, render_template, request, flash, redirect
from models import db, User
# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Bind SQLAlchemy to Flask app
db.init_app(app)
# Create tables on first request
with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
# Render main page
def index():
    """AI is creating summary for index

    Returns:
        [type]: [description]
    """
    return render_template("index.html")


@app.route('/about')
# Render about page
def about():
    """AI is creating summary for about

    Returns:
        [type]: [description]
    """
    return render_template("about.html")


@app.route('/signup', methods=['GET', 'POST'])
# Render signup page
def signup():
    if request.method == 'POST':
        # Create a user with mandatory password hashing
        user = User(username=request.form['username'])
        # The password is hashed before saving
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна!", "success")
        return redirect('/login')
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
# Render login page
def login():
    """AI is creating summary for login

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash("Вы успешно вошли в систему!", "success")
            return redirect('/test')
        else:
            flash('Неверное имя пользователя или пароль.', 'error')

    return render_template("login.html")


@app.route('/test')
# Render test page
def test():
    """AI is creating summary for test

    Returns:
        [type]: [description]
    """
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True)
