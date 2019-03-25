# Author-based functions


def find_author_id(db, author_name):
    names = author_name.split(" ", 1)
    first_name = names[0]
    last_name = names[1]

    author_id = db.execute("""SELECT id FROM author WHERE first_name = ?
                    AND last_name = ?""", (first_name, last_name)).fetchone()

    if author_id:
        return author_id[0]
    else:
        db.execute("""INSERT INTO author(first_name, last_name)
                   VALUES (?,?)""", (first_name, last_name))
        author_id = db.execute("""SELECT id FROM author WHERE first_name = ?
                               AND last_name = ?""",
                               (first_name, last_name)).fetchone()[0]
        return author_id
