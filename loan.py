# Loan based functions

from datetime import datetime as dt, timedelta


def get_user_book_details(db, user_id, book_id):
    book_loan_details = db.execute("""SELECT due_date FROM loan
                                   INNER JOIN copy on copy.id = loan.copy_id
                                   WHERE loan.borrower_id = ?
                                   AND copy.book_id = ?
                                   AND loan.returned = 0
                                   ORDER BY loan.due_date;""",
                                   (user_id, book_id)).fetchone()

    if book_loan_details:
        book_loaned = True
        due_date = book_loan_details['due_date']
    else:
        book_loaned = False
        due_date = ''

    return book_loaned, due_date


def create_loan(db, user_id, book_id):
    copy = db.execute("""SELECT copy.id, copy.hire_period FROM copy WHERE NOT EXISTS
                      (SELECT loan.id FROM loan WHERE loan.copy_id = copy.id
                      AND returned = 0)
                      AND copy.book_id = ?""",
                      (book_id,)).fetchone()

    copy_id = copy['id']
    hire_period = copy['hire_period']

    due_date = (dt.now() + timedelta(days=hire_period)).strftime('%d/%m/%y')

    db.execute("""INSERT INTO loan (copy_id, borrower_id, due_date, returned)
               VALUES (?, ?, ?, ?);""", (copy_id, user_id, due_date, 0))

    return


def end_loan(db, user_id, book_id):
    loan_id = db.execute("""SELECT loan.id
                         FROM loan
                         INNER JOIN copy on copy.id = loan.copy_id
                         WHERE copy.book_id = ?
                         AND loan.borrower_id = ? AND returned = 0""",
                         (book_id, user_id)).fetchone()[0]

    db.execute("""UPDATE loan SET returned = 1 WHERE id=?;""", (loan_id,))

    return


def renew_loan(db, loan_id):
    loan = db.execute("""SELECT due_date,  hire_period FROM loan
                      INNER JOIN copy on copy.id = loan.copy_id
                      WHERE loan.id = ?""", (loan_id,)).fetchone()

    # current_due = dt.strptime(loan['due_date'], '%d/%m/%y')
    hire_period = loan['hire_period']
    new_due = dt.now() + timedelta(days=hire_period)
    new_due_date = new_due.strftime('%d/%m/%y')

    db.execute("""UPDATE loan SET due_date = ? WHERE id = ?;""",
               (new_due_date, loan_id))
