# System Imports
import os

# Module Function Imports
import db_helper
import author
import book 
import user 
import loan
import librarian
import cookies
import utils
from constants import BOOK_COOKIE, ADD_BOOK_COOKIE
from acc_types import AccType

# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
librarian_app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
librarian_app.install(message_plugin)
librarian_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# ====================================================
# Librarian Routes
@librarian_app.get('/librarian/<user_id>/home')
def librarian_home(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    name = librarian.get_librarian_name(db, user_id)
    books = book.get_book_list(db)
    return bottle.template('librarian_pages/librarian_home', user_id=user_id,
                    books=books, name=name,)

@librarian_app.post('/librarian/<user_id>/search')
def librarian_search(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    search_query = bottle.request.forms.get('search_query')
    results = db_helper.get_search_results(db, search_query)

    name = librarian.get_librarian_name(db, user_id)

    return bottle.template('librarian_pages/librarian_search',
                    search_query=search_query,
                    results=results, name=name, user_id=user_id)

@librarian_app.get('/librarian/<user_id>/browse/titles')
def librarian_browse_titles(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    books = book.get_title_list(db)

    name = librarian.get_librarian_name(db, user_id)

    return bottle.template('librarian_pages/librarian_browse_titles', books=books,
                    user_id=user_id, name=name)

@librarian_app.get('/librarian/<user_id>/browse/authors')
def librarian_browse_authors(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    authors = author.get_author_list(db)

    for each in authors:
        author_books = book.get_books_by_author(db, each['id'])
        each['books'] = author_books

    name = librarian.get_librarian_name(db, user_id)

    return bottle.template('librarian_pages/librarian_browse_authors',
                    authors=authors, name=name, user_id=user_id)

@librarian_app.get('/librarian/<user_id>/book/<book_id>')
def librarian_book_details(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    book_details = book.get_book_details(db, book_id)
    copy_availability_details = book.check_copies_available(db, book_id)
    name = librarian.get_librarian_name(db, user_id)

    message = cookies.get_cookie(BOOK_COOKIE, f'/librarian/{user_id}/')

    loan_list = librarian.get_loan_list(db, book_id)
    return bottle.template('librarian_pages/librarian_book_page',
                    book_details=book_details,
                    copy_availability_details=copy_availability_details,
                    name=name, user_id=user_id, loan_list=loan_list,
                    message=message)

@librarian_app.get('/librarian/<user_id>/book_requests')
def view_book_requests(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    name = librarian.get_librarian_name(db, user_id)

    data = db.execute("""SELECT id, title, author_first_name, author_last_name
                      FROM book_request""").fetchall()
    req_id = [x['id'] for x in data]
    book_title = [x['title'] for x in data]
    book_first_name = [x['author_first_name'] for x in data]
    book_last_name = [x['author_last_name'] for x in data]
    book_author = ["{} {}".format(a_, b_) for a_, b_
                   in zip(book_first_name, book_last_name)]

    return bottle.template('librarian_pages/librarian_view_book_requests',
                    name=name, user_id=user_id, book_title=book_title,
                    book_author=book_author, req_id=req_id)

@librarian_app.get('/librarian/<user_id>/book_request/remove/<req_id>')
def remove_book_request(db, user_id, req_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    db.execute("DELETE FROM book_request WHERE id = ?", (req_id,))
    bottle.redirect(f'/librarian/{user_id}/book_requests')

@librarian_app.get('/librarian/<user_id>/books/add')
def add_books(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)
    name = librarian.get_librarian_name(db, user_id)
    message = cookies.get_cookie(ADD_BOOK_COOKIE, cookie_path=f"/librarian/{user_id}")

    return bottle.template('librarian_pages/add_books', name=name, user_id=user_id,
                    message=message)

@librarian_app.post('/librarian/<user_id>/add')
def add_book(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    title = bottle.request.forms.get('title').strip()
    author_name = bottle.request.forms.get('author_name').strip()
    isbn = bottle.request.forms.get('isbn').strip()
    description = bottle.request.forms.get('description').strip()
    publisher = bottle.request.forms.get('publisher').strip()
    year = bottle.request.forms.get('year')
    location = bottle.request.forms.get('location')
    hire_period = bottle.request.forms.get('hire_period')

    author_id = author.find_author_id(db, author_name)
    valid_isbn, isbn_message = book.check_isbn(db, isbn, title, author_id)

    if not valid_isbn:
        cookies.set_cookie(ADD_BOOK_COOKIE, f'{isbn_message}. Add Book failed.',
                   f'/librarian/{user_id}')
        bottle.redirect(f'/librarian/{user_id}/books/add')

    # Book Cover is local path
    cover = bottle.request.files.get('cover')
    if cover is not None:
        try:
            name, ext = os.path.splitext(cover.filename)

            if ext not in ('.png', '.jpg', '.jpeg'):
                cookies.set_cookie(ADD_BOOK_COOKIE,
                        'File extension not allowed. Add Book failed.')
                bottle.redirect(f'/librarian/{user_id}/books/add')

            cover_save_path = book.get_cover_save_path(title, author_name)
            cover_path = cover_save_path + '/' + cover.filename

            if os.path.exists(cover_path):
                os.remove(cover_path)

            cover_path = '/' + cover_path
            cover.save(cover_save_path)

        except AttributeError:
            cover_path = '/static/images/missing_book_cover.jpg'

    # Book Cover is a Remote path
    else:
        cover_path = bottle.request.forms.get('cover') 


    book_id = book.find_book_id(db, title, author_id, isbn, description,
                           publisher, year, cover_path)

    book.insert_copy(db, book_id, hire_period, location)

    bottle.redirect(f'/librarian/{user_id}/book/{book_id}')

@librarian_app.get('/librarian/<user_id>/remove/<book_id>')
def remove_copies(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    name = librarian.get_librarian_name(db, user_id)

    (book_title, first_name, last_name, cover) = db.execute("""SELECT title, first_name, last_name, cover 
                                                        FROM book JOIN author on author.id=author_id 
                                                        WHERE book.id=?""",(book_id,)).fetchone()
    author = first_name + ' ' + last_name

    copies_rows = db.execute("""SELECT copy.id, location, hire_period FROM copy WHERE book_id=?;""",(book_id,)).fetchall()
    checkout_rows = db.execute("""SELECT copy.id, user.first_name, user.last_name FROM loan 
                                    JOIN copy ON copy_id=copy.id 
                                    JOIN user ON user.id=borrower_id
                                    WHERE returned=0 AND book_id=?;""",(book_id,)).fetchall()
    checkout_list = [x['id'] for x in checkout_rows]
    borrower_list = [x['first_name']+' '+x['last_name'] for x in checkout_rows]
    copies_list = [dict(id=x['id'], location=x['location'], hire_period=x['hire_period']) for x in copies_rows]
    for i in range(len(copies_list)):
        if copies_list[i]['location'] == 1:
            copies_list[i]['location'] = 'Downstairs'
        else:
            copies_list[i]['location'] = 'Upstairs'

        copies_list[i]['checkout'] = 'No'
        copies_list[i]['borrower'] = ''

        for j in range(len(checkout_list)):
            if copies_list[i]['id'] == checkout_list[j]:
                copies_list[i]['checkout'] = 'Yes'
                copies_list[i]['borrower'] = borrower_list[j]
                break

    return bottle.template('librarian_pages/librarian_remove_copies', 
                        name=name, copies=copies_list, book_id=book_id, 
                        book_title=book_title, book_cover=cover,
                        author=author, user_id=user_id)

@librarian_app.get('/librarian/<user_id>/remove/<book_id>/<copy_id>')
def remove_copy(db, user_id, book_id, copy_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    # Remove associated child loans
    db.execute("""DELETE FROM loan WHERE copy_id = ?;""", (copy_id,))

    # Remove book if last copy
    num_copies = db.execute("""SELECT COUNT (copy.id)
                            FROM copy
                            WHERE book_id = ?;
                            """, (book_id,)).fetchone()[0]

    db.execute("""DELETE FROM copy WHERE id = ?;""", (copy_id,))
    if num_copies == 1:
        db.execute("""DELETE FROM book WHERE id = ?;""", (book_id,))
        bottle.redirect(f'/librarian/{user_id}/home')
        return

    bottle.redirect(f'/librarian/{user_id}/remove/{book_id}')

@librarian_app.get('/librarian/<user_id>/edit/<book_id>')
def edit_book(db, user_id, book_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    name = librarian.get_librarian_name(db, user_id)

    book_details = book.get_book_details(db, book_id)

    return bottle.template('librarian_pages/edit_book', user_id=user_id, name=name,
                    book_details=book_details)

@librarian_app.post('/librarian/<user_id>/edit')
def edit_book_details(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    book_id = bottle.request.forms.get('book_id')
    title = bottle.request.forms.get('title')
    author_name = bottle.request.forms.get('author_name')
    description = bottle.request.forms.get('description')
    publisher = bottle.request.forms.get('publisher')
    year = bottle.request.forms.get('year')

    cover = bottle.request.files.get('cover')
    if cover:
        name, ext = os.path.splitext(cover.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            cookies.set_cookie(BOOK_COOKIE,
                       'File extension not allowed. Failed to edit book.',
                       cookie_path=f"/librarian/{user_id}/")
            bottle.redirect(f'/librarian/{user_id}/book/{book_id}')

        cover_save_path = book.get_cover_save_path(title, author_name)
        cover_path = cover_save_path + '/' + cover.filename

        if os.path.exists(cover_path):
            os.remove(cover_path)

        cover_path = '/' + cover_path
        cover.save(cover_save_path)

        db.execute("""UPDATE book SET
                        title=?,
                      description = ?,
                      publisher = ?,
                      year = ?,
                      cover = ?
                      WHERE id = ?;""", (title, description, publisher, year,
                                         cover_path, book_id))
    else:
        db.execute("""UPDATE book SET
                title = ?,
                description = ?,
                publisher = ?,
                year = ?
                WHERE id = ?;""", (title, description, publisher, year, book_id))
    bottle.redirect(f'/librarian/{user_id}/book/{book_id}')

@librarian_app.post('/librarian/<user_id>/add_copy')
def add_copy(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    book_id = bottle.request.forms.get('book_id')
    hire_period = bottle.request.forms.get('hire_period')
    num_of_copies = int(bottle.request.forms.get('num_of_copies'))
    location = bottle.request.forms.get('location')

    for i in range(num_of_copies):
        book.insert_copy(db, book_id, hire_period, location)

    bottle.redirect(f'/librarian/{user_id}/book/{book_id}')

@librarian_app.get('/librarian/<user_id>/users/view')
def view_users(db, user_id):
    db_helper.check_auth(user_id, AccType.LIBRARIAN, db)

    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    user_list = user.get_user_list(db)
    for each_user in user_list:
        db_helper.check_fines(db, each_user['id'])
        user_balance = user.get_user_balance(db, each_user['id'])
        each_user['owe'] = True if user_balance < 0 else False
        each_user['balance_str'] = '£{:.2f}'.format(abs(user_balance))

    return bottle.template('librarian_pages/view_users', name=name, user_id=user_id,
                    user_list=user_list)

@librarian_app.get('/librarian/<librarian_id>/users/view/<view_user_profile_id>')
def view_user_profile(db, librarian_id, view_user_profile_id):
    db_helper.check_auth(librarian_id, AccType.LIBRARIAN, db)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = user.get_user_details(db, view_user_profile_id)
    user_join_date = user.get_user_join_date(db, view_user_profile_id)
    user_past_loans = user.get_user_past_loans(db, view_user_profile_id)
    
    # Late Fees
    db_helper.check_fines(db, user_id)
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
                owe=owe,
                join_date=user_join_date)

    name = librarian.get_librarian_name(db, librarian_id)

    return bottle.template('librarian_pages/view_user_profile', name=name,
                    user_id=librarian_id, user=user_dict)
