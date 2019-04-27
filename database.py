import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        conn.close()

def create_users_table(db_file):
    """ create a table """
    db = open_connection(db_file)
    cursor = db.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                        user_name TEXT NOT NULL UNIQUE, \
                                        password TEXT NOT NULL UNIQUE)')
    
    close_connection(db)


def del_table(db_file, table_name):
    db = open_connection(db_file)
    cursor = db.cursor()
    cursor.execute(f'DROP TABLE {table_name}')
    close_connection(db)

def get_all_data(db_file, table_name):
    db = open_connection(db_file)
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
 
    rows = cursor.fetchall()
 
    for row in rows:
        print(row)

def insert_users_data(db_file, *data): 
    db = open_connection(db_file)
    cursor = db.cursor()
    try: 
        with db:
            cursor.execute(f'INSERT INTO users(user_name, password) VALUES(?, ?)', data)
    except sqlite3.IntegrityError:
        pass
        # print('Record already exists')
    finally:
        close_connection(db)


def open_connection(db_file):
    return sqlite3.connect(db_file)

def close_connection(db):
    db.commit()
    db.close()

def get_database_file():
    path = open('database_path').read()
    return path

def close_file(file):
    file.close()

 
def main():
    database_file = get_database_file()
    # del_table(database_file, 'users')
    create_connection(database_file)
    create_users_table(database_file)
    # insert_users_data(database_file, 'BOBBY', 'VERYSECURE')    
    get_all_data(database_file, 'users')


if __name__ == '__main__':
    main()