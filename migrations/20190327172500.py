"""
Caribou migration file
"""


def upgrade(connection):
    sql = """ALTER TABLE book RENAME TO book_old;"""

    connection.execute(sql)

    sql = """CREATE TABLE book (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER NOT NULL,
            isbn VARCHAR(50) NOT NULL UNIQUE,
            cover VARCHAR(255) NULL,
            description VARCHAR(255) NULL,
            publisher VARCHAR(255) NULL,
            year INTEGER NULL,
            FOREIGN KEY (author_id) REFERENCES author(id)
            ); """

    connection.execute(sql)

    c = connection.cursor()

    old_results = c.execute("""SELECT title, author_id, isbn, cover,
                                     description, publisher, year, id
                                     FROM book_old;""").fetchall()
    for b in old_results:
        title = b[0]
        author_id = b[1]
        isbn = str(b[2])
        cover = b[3]
        description = b[4]
        publisher = b[5]
        year = b[6]
        id = b[7]

        sql = """INSERT INTO book (id, title, author_id, isbn, cover, description,
                            publisher, year)
                            VALUES (\"{}\",\"{}\", \"{}\", \"{}\", \"{}\",
                                \"{}\", \"{}\", \"{}\"
                            );""".format(id, title, author_id, isbn, cover,
                                         description, publisher, year)
        connection.execute(sql)

    sql = """DROP TABLE book_old;"""
    connection.execute(sql)

    connection.commit()


def downgrade(connection):
    sql = """ALTER TABLE book RENAME TO book_old;"""

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

    c = connection.cursor()

    old_results = c.execute("""SELECT title, author_id, isbn, cover,
                                     description, publisher, year
                                     FROM book_old;""").fetchall()
    for b in old_results:
        title = b[0]
        author_id = b[1]
        isbn = int(b[2])
        cover = b[3]
        description = b[4]
        publisher = b[5]
        year = b[6]

        sql = """INSERT INTO book (title, author_id, isbn, cover, description,
                            publisher, year)
                            VALUES (\"{}\", \"{}\", \"{}\", \"{}\",
                                    \"{}\", \"{}\", \"{}\"
                            );""".format(title, author_id, isbn, cover,
                                         description, publisher, year)
        print(sql)
        connection.execute(sql)

    connection.commit()
