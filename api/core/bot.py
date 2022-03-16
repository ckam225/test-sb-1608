import sqlite3
from core.settings import MEDIA_URL


def get_connection() -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect('db.sqlite3')
    except sqlite3.Error as error:
        print("SQLITE Error: ", error)
    return conn


def get_all_images():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media;")
        rows = cursor.fetchall()
        for r in rows:
            yield {
                'id': r[0],
                'name': r[1],
                'category': r[2],
                'url': f"{MEDIA_URL}/{r[3]}",
                'created_at': r[4],
                'updated_at': r[5]
            }


def get_unique_categories():
    rows = []
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM media;")
        rows = [r[0] for r in cursor.fetchall()]
    return rows


def add_vote(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT *  FROM vote WHERE telegram_id = ?", (id,))
        if len(cursor.fetchall()) == 0:
            cursor.execute(
                "INSERT INTO vote(id, telegram_id) VALUES( ?, ?)", (id, id))
            conn.commit()
            cursor.close()


users = []
images = get_all_images()
categories = get_unique_categories()


def get_current_image():
    try:
        return next(images)
    except StopIteration:
        print('No images from database')


bot_bag = {}

bot_bag['current_image'] = get_current_image()


def is_register(id):
    return next((user for user in users if user['id'] == id), None)


def authenticate(uid, password):
    user = None
    for u in users:
        if u['uid'] == uid and u['password'] == password:
            user = u
            break
    return user
