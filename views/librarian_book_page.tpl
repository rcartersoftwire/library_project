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
           <div class="large_book_cover">
                <img src={{cover}}>
           </div>
           <div class="book_details">
                <h2>{{title}}</h2>
                <h3>{{author}}</h3>
                <h5>{{publisher}}</h5> 
                <h5>{{year}}</h5>
                <p>{{description}}</p>
           </div>
           
           % include('copy_book_details.tpl', copies=copies,
           %         copies_available=copies_available, next_due=next_due )
        </div>
    </body>

</html>