import bottle
from datetime import date
from models.acc_types import AccType
import services.cookies

def redirect_to_home(db):
    user_id = services.cookies.get_auth_cookie()
    if user_id:
        acc_type =  db.execute('SELECT type FROM user WHERE user.id=?;',(user_id,)).fetchone()
        if acc_type is not None:
            if acc_type['type'] == AccType.LIBRARIAN.value:
                bottle.redirect(f'/librarian/{user_id}/home')
            elif acc_type['type'] == AccType.USER.value:
                bottle.redirect(f'/user/{user_id}/home')
        else:
            services.cookies.del_auth_cookie()

    bottle.redirect('/')

def check_session_acctype():
    session_acctype = services.cookies.get_acctype_cookie()
    if session_acctype:
        return int(session_acctype)
    return None

def check_auth(user_id, acc_type, db):
    existing_user_id = services.cookies.get_auth_cookie()
    if existing_user_id is None:
        raise bottle.HTTPError(401, 'Unauthorized Error')

    # Check for user id matching and acc_type match
    if str(existing_user_id) == str(user_id):
        acc_type_row =  db.execute('SELECT type FROM user WHERE user.id=?;',(user_id,)).fetchone()
        if acc_type.value == acc_type_row['type']:
            return True
        raise bottle.HTTPError(401, 'Unauthorized Error')
    else:
        raise bottle.HTTPError(401, 'Unauthorized Error')

def get_users_search_results(db, search_query, sort_query='last_name'):
    if sort_query is None:
        sort_query = 'last_name'
    search_queries = search_query.split(' ')
    search_pattern = '%'.join(search_queries)
    search_pattern = '%' + search_pattern + '%'
    search_results = db.execute(f"""SELECT user.id
                                FROM user WHERE type=0 AND 
                                ((first_name || ' ' || last_name LIKE ?) OR (last_name || ' ' || first_name LIKE ?)) ORDER BY {sort_query};""",
                                (search_pattern,search_pattern)).fetchall()
    return search_results

def get_search_results(db, search_query):
    search_queries = search_query.split(' ')
    search_pattern = '%'.join(search_queries)
    search_pattern = '%' + search_pattern + '%'
    search_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                author.first_name as first_name,
                                author.last_name as last_name
                                FROM book
                                INNER JOIN author on author.id = book.author_id
                                WHERE book.title LIKE ?
                                OR author.first_name || ' ' ||
                                author.last_name LIKE ?;""",
                                (search_pattern, search_pattern)).fetchall()

    results = [{'id': b['book_id'], 'title': b['title'],
                'author': b['first_name'] + ' ' + b['last_name']}
               for b in search_results]

    for book in results:
        num_copies = db.execute("""SELECT COUNT (copy.id)
                                FROM book
                                INNER JOIN copy on copy.book_id = book.id;
                                """).fetchone()[0]

        active_loans = db.execute("""SELECT COUNT(loan.id)
                                  FROM book
                                  INNER JOIN copy on copy.book_id = ?
                                  INNER JOIN loan on loan.copy_id = copy.id
                                  WHERE loan.returned = 0;""",
                                  (book['id'],)).fetchone()[0]
        if num_copies != 0 and num_copies > active_loans:
            book['available'] = 'Available'
        else:
            book['available'] = 'Unvailable'

    return results

def check_fines(db, user_id):
    # Check current and past loans
    user_loans = db.execute("""SELECT due_date, returned, returned_date
                                 FROM loan WHERE borrower_id=?;""",(user_id,)).fetchall()
    total_fee_payable = 0
    for loan in user_loans:
        due_date = loan['due_date'].split('/')
        due_date = [int(x) for x in due_date]
        due_date = date(due_date[2]+2000, due_date[1], due_date[0])

        if loan['returned'] == 1:
            # Use Returned Date
            prime_date = loan['returned_date'].split('/')
            prime_date = [int(x) for x in prime_date]
            prime_date = date(prime_date[2]+2000, prime_date[1], prime_date[0])
        
        else:
            # Use Today's date
            prime_date = date.today()

        if due_date < prime_date:
            # £0.50 charged per day after due date 
            delta = (prime_date - due_date).days
            total_fee_payable += delta * 0.5

    if total_fee_payable != 0:
        # Assign late fee
        db.execute("""UPDATE user SET late_fee=? WHERE user.id=?;""",(total_fee_payable, user_id))
        # Update Balance
        user_paid = db.execute("""SELECT paid FROM user WHERE user.id=?;""",(user_id,)).fetchone()[0]
        balance = user_paid - total_fee_payable
        db.execute("""UPDATE user SET balance=? WHERE user.id=?;""",(balance, user_id))

