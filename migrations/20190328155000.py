"""
Caribou migration file
"""


def upgrade(connection):
    # Add checkout_date and returned_date column to loan table
    sql = """ALTER TABLE loan ADD COLUMN
             checkout_date VARCHAR(255) NOT NULL
             DEFAULT '';"""
    connection.execute(sql)

    sql = """ALTER TABLE loan ADD COLUMN
             returned_date VARCHAR(255) NOT NULL
             DEFAULT '';"""

    connection.execute(sql)

    connection.commit()


def downgrade(connection):
    pass
