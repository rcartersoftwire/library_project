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

    list_of_borrowers = [[x['id'], x['first_name'] + ' ' + x['last_name']]
                         for x in borrower_list]

    return list_of_borrowers

def get_loan_history(db, book_id):
    loan_history_row = db.execute("""SELECT copy.id, first_name, last_name, 
                                    checkout_date, due_date, returned, 
                                    returned_date FROM loan 
                                    JOIN copy ON copy_id=copy.id 
                                    LEFT JOIN user ON user.id=borrower_id 
                                    WHERE book_id=?;""",(book_id,)).fetchall()

    return loan_history_row