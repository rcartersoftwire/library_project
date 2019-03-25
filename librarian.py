# Librarian functions


def get_librarian_name(db, id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    return name
