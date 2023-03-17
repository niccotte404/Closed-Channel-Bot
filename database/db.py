#-*- coding: utf-8 -*-
import sqlite3

def create_db():
    global curr, connect
    connect = sqlite3.connect("closed_channel.db")
    curr = connect.cursor()
    if connect:
        print("db connect OK")

    # add primary key
    curr.execute("""CREATE TABLE IF NOT EXISTS access(
        link TEXT,
        user_id TEXT,
        access_key TEXT
        )""")
    connect.commit()
    
    
async def add_user(data):
    curr.execute("INSERT INTO access VALUES(?, ?, ?)", tuple(data.values()))
    connect.commit()
    print("user inserted OK")
    
    
async def dell_user(data):
    print(data)
    curr.execute(f"DELETE FROM access WHERE user_id = {data}")
    connect.commit()
    print("user deleted OK")
    
    
def check_user(user):
    users = curr.execute(f"SELECT * FROM access WHERE link = '{user}'").fetchone()
    return users


def check_id(user_id):
    ids = curr.execute(f"SELECT * FROM access WHERE link = '{user_id}'").fetchone()
    return ids


async def add_user_id(username, user_id):
    data = curr.execute(f"SELECT * FROM access WHERE link = '{username}'").fetchone()
    curr.execute(f"DELETE FROM access WHERE link = '{username}'")
    curr.execute(f"INSERT INTO access VALUES(?, ?, ?)", (data[0], user_id, data[2]))
    connect.commit()
    

def all_users():
    data = curr.execute(f"SELECT * FROM access").fetchall()
    return data


def select_access_key(user_id):
    data = curr.execute(f"SELECT * FROM access WHERE user_id = '{user_id}'").fetchone()
    return data[2]