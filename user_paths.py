# Module Function Imports
import db_helper
import author
import book
import user
import loan
import cookies
import utils
from constants import (EDIT_ACC_COOKIE)
from acc_types import AccType

# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
user_app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
user_app.install(message_plugin)
user_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# ====================================================
# User Routes
@user_app.route('/user/<id>/home')
def user_home(db, id):

    db_helper.check_auth(id, AccType.USER, db)

    book_requested = bottle.request.params.get('book_requested')
    if book_requested is not None:
        book_requested = eval(book_requested)
    else:
        book_requested = False

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, id)

    books = book.get_book_list(db)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)
    return bottle.template('user_pages/user_home', books=books, user=user_dict,
                    book_requested=book_requested)

@user_app.post('/user/<user_id>/account')
def pay_fees(db, user_id):
    fees_paid = bottle.request.forms.get('payFees')
    paid = user.get_user_paid(db, user_id)
    paid += float(fees_paid)
    user.put_user_paid(db, user_id, paid)
    db_helper.check_fines(db, user_id)
    bottle.redirect(f'/user/{user_id}/account')


@user_app.get('/user/<user_id>/account')
def user_account(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    db_helper.check_fines(db, user_id)
    
    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)
    user_join_date = user.get_user_join_date(db, user_id)
    user_past_loans = user.get_user_past_loans(db, user_id)
    
    user_balance = user.get_user_balance(db, user_id)
    owe = True if user_balance < 0 else False
    user_balance_str = '£{:.2f}'.format(abs(user_balance))

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                prof_pic=user_prof_pic,
                past_loans=user_past_loans,
                balance_str=user_balance_str,
                balance=user_balance,
                owe=owe,
                join_date=user_join_date)

    return bottle.template('user_pages/user_account', user=user_dict)


@user_app.post('/user/<user_id>/search')
def user_search(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    search_query = bottle.request.forms.get('search_query')
    results = db_helper.get_search_results(db, search_query)

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return bottle.template('user_pages/user_search', search_query=search_query,
                    results=results, user=user_dict)


@user_app.get('/user/<user_id>/browse/authors')
def user_browse_authors(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    authors = author.get_author_list(db)

    for each in authors:
        author_books = book.get_books_by_author(db, each['id'])
        each['books'] = author_books

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return bottle.template('user_pages/user_browse_authors', authors=authors,
                    user=user_dict)


@user_app.get('/user/<user_id>/book/<book_id>')
def user_book_details(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    book_details = book.get_book_details(db, book_id)
    copy_availability_details = book.check_copies_available(db, book_id)

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)

    book_loaned, due_date = loan.get_user_book_details(db, user_id, book_id)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return bottle.template('user_pages/user_book_page', book_details=book_details,
                    user=user_dict, book_loaned=book_loaned, due_date=due_date,
                    copy_availability_details=copy_availability_details)


@user_app.get('/user/<user_id>/browse/titles')
def user_browse_titles(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    books = book.get_title_list(db)

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return bottle.template('user_pages/user_browse_titles', books=books,
                    user=user_dict)


@user_app.get('/user/<user_id>/borrow/<book_id>')
def borrow(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    loan.create_loan(db, user_id, book_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/return/<book_id>')
def return_book(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    loan.end_loan(db, user_id, book_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/renew/<book_id>')
def renew_book(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    loan_id = book.find_loan_id(db, user_id, book_id)

    loan.renew_loan(db, loan_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/book_request')
def book_request(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)
    user_join_date = user.get_user_join_date(db, user_id)
    user_past_loans = user.get_user_past_loans(db, user_id)

    user_dict = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                past_loans=user_past_loans,
                join_date=user_join_date)

    return bottle.template('user_pages/user_book_request', user=user_dict)


@user_app.post('/user/<user_id>/book_request')
def add_book_request(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    title = bottle.request.forms.get('title').strip()
    author_name = bottle.request.forms.get('author_name').strip()

    names = author_name.split(" ", 1)
    first_name = names[0]
    if len(names) == 1:
        last_name = ''
    else:
        last_name = names[1]

    db.execute("""INSERT INTO book_request(title, author_first_name, author_last_name)
                VALUES (?,?,?)""", (title, first_name, last_name))

    bottle.redirect(f'/user/{user_id}/home?book_requested=True')


@user_app.get('/user/<user_id>/account/close')
def close_user_account(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    (user_id, user_first_name, user_last_name, user_loan_count,
    user_current_loans, user_prof_pic) = user.get_user_details(db, user_id)
    if len(user_current_loans) == 0 :
        db.execute("DELETE FROM loan WHERE borrower_id = ?;", (user_id,))
        db.execute("DELETE FROM user WHERE user.id = ?;", (user_id,))
        bottle.redirect('/logout')
    else:
        print ("User still has outstanding loans!")
        bottle.redirect(f'/user/{user_id}/account')


@user_app.get('/user/<user_id>/account/edit')
def edit_user_account(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    message = cookies.get_cookie(EDIT_ACC_COOKIE)

    (user_id, user_first_name, user_last_name, user_loan_count,
    user_loans, user_prof_pic) = user.get_user_details(db, user_id)
    user_join_date = user.get_user_join_date(db, user_id)
    user_past_loans = user.get_user_past_loans(db, user_id)
    (username) = db.execute("SELECT username FROM user WHERE id=?;",(user_id,)).fetchone()

    user_dict = dict(id=user_id,
                username=username['username'],
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                prof_pic=user_prof_pic,
                past_loans=user_past_loans,
                join_date=user_join_date)


    return bottle.template('user_pages/edit_user_account', message=message, user=user_dict)


@user_app.post('/user/<user_id>/account/edit')
def edit_user_account_post(db, user_id):
    db_helper.check_auth(user_id, AccType.USER, db)
    first_name = bottle.request.forms.get('first_name').capitalize()
    last_name = bottle.request.forms.get('last_name').capitalize()
    username = bottle.request.forms.get('username')
    old_password = bottle.request.forms.get('old_password')
    new_password = bottle.request.forms.get('new_password')
    prof_pic = bottle.request.files.get('prof_pic')

    db.execute("""UPDATE user SET
                    first_name = ?,
                    last_name = ?,
                    username = ?
                    WHERE id = ?;""", (first_name, last_name, username,
                                        user_id))
    if prof_pic:
        try:
            name, ext = os.path.splitext(prof_pic.filename)

            if ext not in ('.png', '.jpg', '.jpeg'):
                cookies.set_cookie(EDIT_ACC_COOKIE,
                        'File extension not allowed. Adding profile pic failed.')
                bottle.redirect(f'/user/{user_id}/account')

            save_path = f"""static/images/prof_pics/{username}"""
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            prof_pic.save(save_path)
            profile_pic_path = '/' + save_path + '/' + prof_pic.filename
            db.execute("""UPDATE user SET
                    prof_pic = ?
                    WHERE id = ?;""", (profile_pic_path,
                                        user_id))
        except:
            cookies.set_cookie(EDIT_ACC_COOKIE,
                'Profile Pic Update Failed')
            bottle.redirect(f'/user/{user_id}/account/edit')

    pwd_verified = False
    if old_password is not None and old_password != '':
        verify_pwd = db.execute("""SELECT password FROM user WHERE user.id=?""",(user_id,)).fetchone()
        print (verify_pwd['password'])
        if old_password == verify_pwd['password']:
            pwd_verified = True
        else:
            cookies.set_cookie(EDIT_ACC_COOKIE,
                'Incorrect Password')
            bottle.redirect(f'/user/{user_id}/account/edit')

    if pwd_verified:
        db.execute("""UPDATE user SET
                        password = ?
                        WHERE id = ?;""", (new_password,
                                            user_id))


    cookies.set_cookie(EDIT_ACC_COOKIE,
                    'Account Updated')
    bottle.redirect(f'/user/{user_id}/account/edit')


