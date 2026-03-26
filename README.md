# task-manager-study

Week 3 adds SQLite persistence with Flask-SQLAlchemy and full CRUD for tasks.

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

## Notes

- Database file is created automatically as `tasks.db` when app starts.
- If the table does not exist, it is created automatically.