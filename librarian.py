# Librarian functions


def get_librarian_name(db, id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    return name
    
def get_loan_list(db, book_id):
    borrower_list = db.execute("""SELECT user.id, first_name, last_name FROM loan
                               JOIN copy on copy_id=copy.id
                               JOIN user on borrower_id=user.id
                               WHERE book_id = ? AND returned = 0""",
                               (book_id,)).fetchall()

    list_of_borrowers = [[x['id'] ,x['first_name']+' '+x['last_name']]
                         for x in borrower_list]

    return list_of_borrowers

