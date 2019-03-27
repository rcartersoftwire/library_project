"""
Caribou migration file
"""


def upgrade(connection):
    sql = """ALTER TABLE user ADD COLUMN
             join_date VARCHAR(255) DEFAULT '25/03/2019';"""

    connection.execute(sql)

    connection.commit()


def downgrade(connection):
    pass
