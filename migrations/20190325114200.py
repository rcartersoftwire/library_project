"""
Caribou migration file
"""


def upgrade(connection):
    sql = """CREATE TABLE IF NOT EXISTS author(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NULL
                );"""

    connection.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS book (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                author_id INTEGER NOT NULL,
                isbn INTEGER NOT NULL UNIQUE,
                cover VARCHAR(255) NULL,
                description VARCHAR(255) NULL,
                publisher VARCHAR(255) NULL,
                year INTEGER NULL,
                FOREIGN KEY (author_id) REFERENCES author(id)
                ); """

    connection.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS copy (
                id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                location INTEGER NULL, -- enumerate possible locations
                hire_period INTEGER NOT NULL, -- number of days
                FOREIGN KEY(book_id) REFERENCES book(id)
                );"""

    connection.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS user (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                type INT NOT NULL -- 0 = borrower, 1 =  librarian
                );"""

    connection.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS loan (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                copy_id INTEGER NOT NULL,
                borrower_id INTEGER NOT NULL,
                due_date VARCHAR(255) NOT NULL,
                returned INTEGER NOT NULL, -- 0 = false, 1 = true
                FOREIGN KEY (copy_id) REFERENCES copy(id),
                FOREIGN KEY (borrower_id) REFERENCES user(id)
                ); """

    connection.execute(sql)

    connection.commit()


def downgrade(connection):

    connection.execute("DROP TABLE author")
    connection.execute("DROP TABLE book")
    connection.execute("DROP TABLE copy")
    connection.execute("DROP TABLE user")
    connection.execute("DROP TABLE loan")
