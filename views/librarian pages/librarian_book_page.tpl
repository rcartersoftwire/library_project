<html>
    <head>
        <title>Library | {{title}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
        <link rel="stylesheet" type="text/css" href="/static/style/user_book_page.css">
    </head>
    <body>
            % include('librarian_header_bar.tpl')
            % include('librarian_sidebar.tpl')
        <div class="main_page">
            % include('book_details', title=title, author=author, publisher=publisher,
            %         year=year, description=description)
            % include('copy_book_details.tpl', copies=copies,
            %         copies_available=copies_available, next_due=next_due )
        </div>
    </body>

</html>