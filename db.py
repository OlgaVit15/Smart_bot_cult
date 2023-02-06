import sqlite3
from sqlite3 import Error
from os import path


def get_script_dir():
    abs_path = path.abspath(__file__)
    return path.dirname(abs_path)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


DB_NAME = 'places.sqlite'
DB_FILE = get_script_dir() + path.sep + DB_NAME


def getPlaces_create_btn():
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute("""PRAGMA foreign_keys = ON""")
    print("Подключение успешно")
    cur.execute(
        "SELECT Places.name FROM Places;"
    )
    places = cur.fetchall()
    conn.close()
    return places


def getPlaces(text):
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute("""PRAGMA foreign_keys = ON""")
    print("Подключение успешно")
    cur.execute(
        f"SELECT * FROM Places WHERE name = '{text}';"
    )
    inf = cur.fetchone()
    conn.close()
    return inf


def createTable():
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute("""PRAGMA foreign_keys = ON""")
    print("Подключение успешно")
    cur.execute(""" CREATE TABLE IF NOT EXISTS Places (
                                        name text,
                                        inf text,
                                        url text
                                    ); """)
    print("Таблица создана")
    cur.execute("create unique index PlacesInformation_name, inf on Places ( name, inf )")
    print("OK")
    conn.commit()
    conn.close()


def insertValuesInDB():
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    # cur.execute(
    #     "INSERT OR IGNORE INTO Places VALUES ('Памятник Первопоселенцу', 'памятник', 'lastochka.img')"
    # )
    print("Значения внесены")
    conn.commit()
    conn.close()


# conn = create_connection(DB_FILE)
# cur = conn.cursor()
# # cur.execute("DELETE FROM Places WHERE rowid = 3;")
# # print("Deleted")
# # cur.execute("UPDATE Places SET name = 'Памятник Ласточка' WHERE rowid=0")
# # print("changed")
# cur.execute("SELECT * FROM Places")
# p = cur.fetchall()
# print(p)
# # insertValuesInDB()
