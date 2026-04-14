# task-manager-study

This project is a task manager made with Flask.

## What We Did

- created a home page
- created a register page
- created a login page
- created a tasks page
- added user registration with username, email, and password
- added user login with username or email
- added logout
- added password hashing using Flask-Bcrypt
- added protected routes for logged-in users
- added task create feature
- added task view feature
- added task update feature
- added task delete feature
- added task filter for all, completed, and pending tasks
- used SQLite database to store data
- used HTML templates for frontend pages
- used Bootstrap for styling

## Files Used

- `app.py` for main Flask app, models, and routes
- `templates/index.html` for home page
- `templates/register.html` for register page
- `templates/login.html` for login page
- `templates/tasks.html` for tasks page
- `requirements.txt` for project dependencies
- `week1_practice.py` for Python practice

## Database

This project uses SQLite.

It has:

- User model
- Task model

## Routes

- `/`
- `/register`
- `/login`
- `/logout`
- `/tasks`
- `/tasks/add`
- `/tasks/<int:task_id>/edit`
- `/tasks/<int:task_id>/delete`

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the project:

```bash
python app.py
```