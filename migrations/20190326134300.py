"""
Caribou migration file
"""


def upgrade(connection):
    sql = """ALTER TABLE user ADD COLUMN
             join_date VARCHAR(255) DEFAULT '25/03/2019';"""

    connection.execute(sql)

    # Adding Book Request Table
    sql = """CREATE TABLE IF NOT EXISTS book_request(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                author_first_name VARCHAR(255) NOT NULL,
                author_last_name VARCHAR(255) NOT NULL
                );"""

    connection.execute(sql)


    connection.commit()


def downgrade(connection):
    pass
