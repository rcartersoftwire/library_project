from datetime import date
import services.tools

class User:
    def __init__(self, db, user_id):
        (self.id, self.first_name, self.last_name, self.loan_count,
            self.loans, self.prof_pic) = User.get_user_details(db, user_id)
        self.name = " ".join([self.first_name, self.last_name])
        self.join_date = User.get_user_join_date(db, user_id)
        self.past_loans = User.get_user_past_loans(db, user_id)
        self.username = User.get_user_username(db, user_id)
        self.balance = User.get_user_balance(db, user_id)
        self.owe = True if self.balance < 0 else False
        self.balance_str = '£{:.2f}'.format(abs(self.balance))


    # User based functions
    @staticmethod
    def get_user_details(db, user_id):
        user_details = db.execute("""SELECT first_name, last_name FROM user
                        WHERE user.id = ?;""", (user_id,)).fetchone()

        user_loan_results = db.execute("""SELECT copy_id, checkout_date, book.id as book_id, book.title as title,
                                    author.first_name as first_name,
                                    author.last_name as last_name,
                                    loan.due_date as due_date
                                    FROM loan
                                    INNER JOIN copy on copy.id = loan.copy_id
                                    INNER JOIN book on book.id = copy.book_id
                                    INNER JOIN author on
                                    author.id = book.author_id
                                    WHERE loan.borrower_id = ? AND
                                    loan.returned = 0;""", (user_id,))

        user_first_name = user_details['first_name']
        user_last_name = user_details['last_name']

        user_loans = []
        for l in user_loan_results:
            today = date.today().strftime("%d/%m/%y")
            late = services.tools.check_if_late(l['due_date'], today)
            user_loans.append({'book_id': l['book_id'], 'title': l['title'],
                        'author': l['first_name'] + ' ' + l['last_name'],
                        'due_date': l['due_date'],
                        'checkout_date': l['checkout_date'],
                        'late': late,
                        'copy_id': l['copy_id']})

        user_loan_count = len(user_loans)

        user_profile_pic = db.execute("""SELECT prof_pic FROM user
                                    WHERE id=?;""", (user_id,)
                                    ).fetchone()['prof_pic']

        return (user_id, user_first_name, user_last_name, user_loan_count,
                user_loans, user_profile_pic)

    @staticmethod
    def get_user_username(db, user_id):
        return db.execute("SELECT username FROM user WHERE id=?;",(user_id,)).fetchone()['username']

    @staticmethod
    def get_user_list(db, list_of_ids=None, sort=None, order='ASC'):
        if list_of_ids is not None:
            user_results = list_of_ids
        else:
            if sort is not None:
                user_results = db.execute(f"""SELECT id FROM user WHERE type = 0 ORDER BY {sort} {order};
                            """).fetchall()
            else:
                user_results = db.execute(f"""SELECT id FROM user WHERE type = 0 ORDER BY last_name {order};
                            """).fetchall()
        user_list = []

        for user in user_results:
            user_list.append(User(db, user['id']))

        return user_list

    @staticmethod   
    def get_user_balance(db, user_id):
        return db.execute("""SELECT balance FROM user WHERE user.id=?;""",(user_id,)).fetchone()[0]

    @staticmethod
    def get_user_paid(db, user_id):
        return db.execute("""SELECT paid FROM user WHERE user.id=?;""",(user_id,)).fetchone()[0]

    @staticmethod
    def put_user_paid(db, user_id, paid):
        db.execute("""UPDATE user SET paid=? WHERE user.id=?;""",(paid, user_id))
        return

    @staticmethod
    def get_user_past_loans(db, id):
        past_loan_results = db.execute("""SELECT copy_id, returned_date, checkout_date,
                                        book.id as book_id, book.title as title,
                                    author.first_name as first_name,
                                    author.last_name as last_name,
                                    loan.due_date as due_date
                                    FROM loan
                                    INNER JOIN copy on copy.id = loan.copy_id
                                    INNER JOIN book on book.id = copy.book_id
                                    INNER JOIN author on
                                    author.id = book.author_id
                                    WHERE loan.borrower_id = ? AND
                                    loan.returned = 1;""", (id,))
        past_loans = []
        for l in past_loan_results:
            late = services.tools.check_if_late(l['due_date'], l['returned_date'])

            past_loans.append({'book_id': l['book_id'], 'title': l['title'],
                        'author': l['first_name'] + ' ' + l['last_name'],
                        'checkout_date': l['checkout_date'],
                        'due_date' : l['due_date'],
                        'late': late,
                        'returned_date': l['returned_date'],
                        'copy_id': l['copy_id']})

        return past_loans

    @staticmethod
    def get_user_join_date(db, id):
        join_date = db.execute("SELECT join_date FROM user WHERE id =?;",
                            (id,)).fetchone()[0]

        return join_date
