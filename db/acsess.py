import sqlite3

###########データベース操作##################
con = sqlite3.connect('db/auth.sqlite3')

# データベース操作のためのcurを作成
cur = con.cursor()

# テーブル生成
cur.execute('create table if not exists \
            auth(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                username TEXT, \
                hashed_password TEXT, \
                disabled TEXT)')


def search_username(cur,username:str):
    sql = 'select * from auth where username like "' + username + '"'
    cur.execute(sql)
    res:tuple = cur.fetchone()
    if res == None:
        return None
    return {'id': int(res[0]), 'username': str(res[1]), 'hashed_password': str(res[2]), 'disabled': str(res[3])}

def insert_registration(cur,username:str,hashed_password:str,disabled:str='False'):
    in_data = (username,hashed_password,disabled)
    cur.execute(f'insert into auth (username, hashed_password, disabled) values (?, ?, ?)', in_data)
    con.commit()

def update_pw(cur,username:str,hashed_password:str):
    in_data = (hashed_password,username)
    cur.execute(f'update auth set hashed_password = ? WHERE username = ?', in_data)
    con.commit()