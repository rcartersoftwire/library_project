"""
Caribou migration file
"""


def upgrade(connection):
    # Add Fines Column to user
    sql = """ALTER TABLE user ADD COLUMN
             late_fee FLOAT NOT NULL
             DEFAULT 0;"""

    connection.execute(sql)

    sql = """ALTER TABLE user ADD COLUMN
            paid FLOAT NOT NULL
            DEFAULT 0;"""

    connection.execute(sql)

    sql = """ALTER TABLE user ADD COLUMN
            balance FLOAT NOT NULL
            DEFAULT 0;"""

    connection.execute(sql)

    connection.commit()


def downgrade(connection):
    pass
