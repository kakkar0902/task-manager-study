from datetime import datetime
from functools import wraps

from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "change-this-in-production"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = db.session.get(User, user_id) if user_id else None


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user is not None:
        return redirect(url_for("tasks"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.query.filter(or_(User.username == username, User.email == email)).first():
            error = "Username or email already exists."
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login", success="Registration complete. Please log in."))

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("tasks"))

    error = None

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            or_(User.username == identifier, User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(password):
            error = "Invalid username/email or password."
        else:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("tasks"))

    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/tasks")
@login_required
def tasks():
    all_tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template("tasks.html", tasks=all_tasks)


@app.route("/tasks/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return redirect(url_for("tasks", error="Task title is required."))

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("tasks"))


@app.route("/tasks/<int:task_id>/edit", methods=["POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return redirect(url_for("tasks", error="Task title is required."))

    task.title = title
    task.description = description
    task.completed = request.form.get("completed") == "on"
    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks"))

if __name__ == "__main__":
    app.run(debug=True)