from sqlite3 import Error
import sqlite3


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_images_table():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS images (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        photo blob
                                    ); """
    return sql_create_projects_table


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(Id, name, photo):
    try:
        sqliteConnection = sqlite3.connect('pythonsqlite.db')
        cursor = sqliteConnection.cursor()

        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO images
                                  (id, name, photo) VALUES (?, ?, ?)"""

        # Convert data into tuple format
        data_tuple = (Id, name, photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")


def select_images():
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    sqliteConnection = sqlite3.connect('pythonsqlite.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM images")

    rows = cursor.fetchall()

    return rows


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_table(conn, create_images_table())
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def main():
    create_connection(r"pythonsqlite.db")
