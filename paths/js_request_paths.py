# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
request_app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
request_app.install(message_plugin)
request_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))


# JS Request Paths
@request_app.get('/get_username_list/<username>')
def get_username_list(db, username):
    username_in_db = db.execute("SELECT id FROM user WHERE username =?",
                                (username,)).fetchall()
    if username_in_db:
        return {'nameTaken': True}
    else:
        return {'nameTaken': False}

@request_app.get('/get_book_location/<book_id>')
def get_book_location(db, book_id):
    all_copies_location = db.execute("""SELECT copy.id, location
                                     FROM copy WHERE book_id = ?""",
                                     (book_id,)).fetchall()

    unavailable_copies = db.execute("""SELECT copy.id FROM copy
                                    JOIN loan on copy_id=copy.id
                                    WHERE loan.returned = 0 AND book_id = ?""",
                                    (book_id,)).fetchall()

    list_of_unavailable_copies = [x['id'] for x in unavailable_copies]

    downstairs = 0
    upstairs = 0
    for copy in all_copies_location:
        if copy['id'] not in list_of_unavailable_copies:
            if copy['location'] == 1:
                downstairs += 1
            else:
                upstairs += 1

    return {'downstairs': downstairs, 'upstairs': upstairs}

