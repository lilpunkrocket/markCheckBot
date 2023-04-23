import sqlite3


async def initialize_db():
    global db, cur
    db = sqlite3.connect('../main.db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS students(user_id TEXT PRIMARY KEY, token TEXT)')
    db.commit()


async def close_db():
    db.close()


async def create_user(user_id):
    user = cur.execute('SELECT 1 FROM students WHERE user_id=\'{id}\''.format(id=user_id)).fetchone()
    if not user:
        cur.execute('INSERT INTO students(user_id) VALUES (\'{id}\')'.format(id=user_id))
        db.commit()


async def add_token(user_id, token):
    cur.execute('UPDATE students SET token = \'{token}\' WHERE user_id = \'{id}\''.format(token=token, id=user_id))
    db.commit()


async def get_user_token(user_id):
    token = cur.execute('SELECT token FROM students WHERE user_id = \'{id}\''.format(id=user_id)).fetchone()
    if not token:
        raise ValueError
    return token[0]


async def delete_user(user_id):
    cur.execute('DELETE FROM students WHERE user_id=\'{id}\''.format(id=user_id))
    db.commit()