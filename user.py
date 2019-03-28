# User based functions


def get_user_details(db, id):
    user_details = db.execute("""SELECT id, first_name, last_name FROM user
                      WHERE user.id = ?;""", (id,)).fetchone()

    user_loan_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                   author.first_name as first_name,
                                   author.last_name as last_name,
                                   loan.due_date as due_date
                                   FROM loan
                                   INNER JOIN copy on copy.id = loan.copy_id
                                   INNER JOIN book on book.id = copy.book_id
                                   INNER JOIN author on
                                   author.id = book.author_id
                                   WHERE loan.borrower_id = ? AND
                                   loan.returned = 0;""", (id,))

    user_id = user_details['id']
    user_first_name = user_details['first_name']
    user_last_name = user_details['last_name']

    user_loans = [{'book_id': l['book_id'], 'title': l['title'],
                   'author': l['first_name'] + ' ' + l['last_name'],
                   'due_date': l['due_date']} for l in user_loan_results]

    user_loan_count = len(user_loans)

    user_profile_pic = db.execute("""SELECT prof_pic FROM user WHERE id=?;""", (user_id,)).fetchone()['prof_pic']

    return (user_id, user_first_name, user_last_name, user_loan_count,
            user_loans, user_profile_pic)


def get_user_list(db):
    user_results = db.execute("""SELECT id FROM user WHERE type = 0 ORDER BY last_name;
                              """).fetchall()

    user_list = []

    for user in user_results:
        (user_id, user_first_name, user_last_name, user_loan_count,
         user_loans, user_prof_pic) = get_user_details(db, user['id'])

        user_name = user_first_name + ' ' + user_last_name

        user_list.append({'user_id': user_id, 'name': user_name,
                          'loan_count': user_loan_count,
                          'loans': user_loans, 'prof_pic': user_prof_pic})

    return user_list


def get_user_past_loans(db, id):
    past_loan_results = db.execute("""SELECT book.id as book_id, book.title as title,
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

    past_loans = [{'book_id': l['book_id'], 'title': l['title'],
                  'author': l['first_name'] + ' ' + l['last_name']}
                  for l in past_loan_results]

    return past_loans


def get_user_join_date(db, id):
    join_date = db.execute("SELECT join_date FROM user WHERE id =?;",
                           (id,)).fetchone()[0]

    return join_date
