"""
Caribou migration file
"""


def upgrade(connection):
    # Adding Book Request Table
    sql = """CREATE TABLE IF NOT EXISTS book_request(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                author_first_name VARCHAR(255) NOT NULL,
                author_last_name VARCHAR(255) NOT NULL
                );"""

    connection.execute(sql)

    # Adding photo path
    sql = """ALTER TABLE user ADD COLUMN
             prof_pic VARCHAR(255)
             DEFAULT '/static/images/unknown-user.jpg';"""
    connection.execute(sql)

    connection.commit()


def downgrade(connection):
    pass
