# task-manager-study

This project includes Week 3 (task CRUD with SQLite) and Week 4 (authentication with user registration/login and protected routes).

## Setup

1. Activate your virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open http://127.0.0.1:5000/ and click "Go to Tasks".

## CRUD Features

- Create: add a task from the create form.
- Read: all tasks are listed on the tasks page.
- Update: edit title/description/completed state and click Update.
- Delete: click Delete for a task.

## Week 4 Authentication Features

- Register: create a user account with username, email, and password.
- Login: sign in using username or email.
- Password Hashing: passwords are stored securely with `Flask-Bcrypt`.
- Protected Routes: `/tasks` and task CRUD endpoints require login.
- Logout: clear session and return to home page.

## Notes

- Database file is created automatically as `tasks.db` when app starts.
- If the table does not exist, it is created automatically.