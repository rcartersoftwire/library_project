<html>
    <head>
        <title>Library | {{title}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
        <link rel="stylesheet" type="text/css" href="/static/style/book_page.css">
    </head>
    <body>
            % include('header_bar.tpl')
            % include('visitor_side_bar.tpl')
        <div class="main_page">
           <div class="large_book_cover">
                <img src={{cover}}>
           </div>
           <div class="book_details">
                <h2>{{title}}</h2>
                <h3>{{author}}</h3>
                <h5>{{publisher}}</h5> 
                <h5>{{year}}</h5>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
           </div>
           % include('copy_book_details.tpl', copies=copies,
           %         copies_available=copies_available, next_due=next_due )
        </div>
    </body>

</html>