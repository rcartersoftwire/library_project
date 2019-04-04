# Module Function Imports
import models.author
import models.book
from models.user import User
from models.acc_types import AccType

import services.db_helper
import services.loan
import services.cookies
import services.tools

from config import database_file

# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
user_app = bottle.Bottle()

# Database Configuration
user_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# ====================================================
# User Routes
@user_app.route('/user/<user_id>/home')
def user_home(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    user = User(db, user_id)

    # Check for request book confirmation
    book_requested = bottle.request.params.get('book_requested')
    if book_requested is not None:
        book_requested = eval(book_requested)
    else:
        book_requested = False

    # Check for search query parameter
    search_query = bottle.request.params.get('search')
    if search_query is not None:
        books = services.db_helper.get_search_results(db, search_query)
    else:
        search_query = ''
        books = models.book.Book.get_book_list(db)

    return bottle.template('user_pages/user_home', books=books, user=user,
                    book_requested=book_requested, search=search_query)

@user_app.post('/user/<user_id>/account')
def pay_fees(db, user_id):
    fees_paid = bottle.request.forms.get('payFees')

    paid = User.get_user_paid(db, user_id)
    paid += float(fees_paid)
    User.put_user_paid(db, user_id, paid)
    
    services.db_helper.check_fines(db, user_id)
    bottle.redirect(f'/user/{user_id}/account')


@user_app.get('/user/<user_id>/account')
def user_account(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    services.db_helper.check_fines(db, user_id)
    
    user_dict = User(db, user_id)

    return bottle.template('user_pages/user_account', user=user_dict)


@user_app.post('/user/<user_id>/search')
def user_search(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    search_query = bottle.request.forms.get('search_query')
    if search_query == '':
        services.db_helper.redirect_to_home(db)
    
    bottle.redirect(f'/user/{user_id}/home?search={search_query}')


@user_app.get('/user/<user_id>/browse/authors')
def user_browse_authors(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    authors = models.author.get_author_list(db)

    for each in authors:
        author_books = models.book.Book.get_books_by_author(db, each['id'])
        each['books'] = author_books

    user_dict = User(db, user_id)

    return bottle.template('user_pages/user_browse_authors', authors=authors,
                    user=user_dict)


@user_app.get('/user/<user_id>/book/<book_id>')
def user_book_details(db, user_id, book_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    book_details = models.book.Book.get_book_details(db, book_id)
    copy_availability_details = models.book.Book.check_copies_available(db, book_id)
    book_loaned, due_date = services.loan.get_user_book_details(db, user_id, book_id)

    user_dict = User(db, user_id)

    return bottle.template('user_pages/user_book_page', book_details=book_details,
                    user=user_dict, book_loaned=book_loaned, due_date=due_date,
                    copy_availability_details=copy_availability_details)


@user_app.get('/user/<user_id>/browse/titles')
def user_browse_titles(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    books = models.book.Book.get_title_list(db)

    user_dict = User(db, user_id)

    return bottle.template('user_pages/user_browse_titles', books=books,
                    user=user_dict)


@user_app.get('/user/<user_id>/borrow/<book_id>')
def borrow(db, user_id, book_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    services.loan.create_loan(db, user_id, book_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/return/<book_id>')
def return_book(db, user_id, book_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    services.loan.end_loan(db, user_id, book_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/renew/<book_id>')
def renew_book(db, user_id, book_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    loan_id = models.book.Book.find_loan_id(db, user_id, book_id)

    services.loan.renew_loan(db, loan_id)

    bottle.redirect(f'/user/{user_id}/book/{book_id}')


@user_app.get('/user/<user_id>/book_request')
def book_request(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    user_dict = User(db, user_id)

    return bottle.template('user_pages/user_book_request', user=user_dict)


@user_app.post('/user/<user_id>/book_request')
def add_book_request(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
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
    services.db_helper.check_auth(user_id, AccType.USER, db)
    user = User(db, user_id)
    if len(user.loan_count) == 0 :
        db.execute("DELETE FROM loan WHERE borrower_id = ?;", (user_id,))
        db.execute("DELETE FROM user WHERE user.id = ?;", (user_id,))
        bottle.redirect('/logout')
    else:
        print ("User still has outstanding loans!")
        bottle.redirect(f'/user/{user_id}/account')


@user_app.get('/user/<user_id>/account/edit')
def edit_user_account(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
    message = services.cookies.get_cookie(services.cookies.EDIT_ACC_COOKIE)

    user_dict = User(db, user_id)

    return bottle.template('user_pages/edit_user_account', message=message, user=user_dict)


@user_app.post('/user/<user_id>/account/edit')
def edit_user_account_post(db, user_id):
    services.db_helper.check_auth(user_id, AccType.USER, db)
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
            services.cookies.set_cookie(services.cookies.EDIT_ACC_COOKIE,
                'Profile Pic Update Failed')
            bottle.redirect(f'/user/{user_id}/account/edit')

    pwd_verified = False
    if old_password is not None and old_password != '':
        verify_pwd = db.execute("""SELECT password FROM user WHERE user.id=?""",(user_id,)).fetchone()
        print (verify_pwd['password'])
        if old_password == verify_pwd['password']:
            pwd_verified = True
        else:
            services.cookies.set_cookie(services.cookies.EDIT_ACC_COOKIE,
                'Incorrect Password')
            bottle.redirect(f'/user/{user_id}/account/edit')

    if pwd_verified:
        db.execute("""UPDATE user SET
                        password = ?
                        WHERE id = ?;""", (new_password,
                                            user_id))


    services.cookies.set_cookie(services.cookies.EDIT_ACC_COOKIE,
                    'Account Updated')
    bottle.redirect(f'/user/{user_id}/account/edit')


