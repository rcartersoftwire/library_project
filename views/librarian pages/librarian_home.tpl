<html>
        <head>
            <title>Library </title>
            <link rel="stylesheet" type="text/css" href="/static/style/global.css">
            <link rel="stylesheet" type="text/css" href="/static/style/book_display.css">
        </head>
    <body>
        % include('librarian_header_bar.tpl')
        % include('librarian_sidebar.tpl')
        <div class="main_page">
            <ul class="browse_filters">
                <li>Browse by:</li>
                <li><a href="/browse_title">Title</a></li>
                <li><a href="/browse_author">Author</a></li>
                <li><a href="/browse_genre">Genre</a></li>
            </ul>
            <div class="book_display">
                % for book in books:
                    <div class="book_tile">
                        <img class ="book_cover" src="/static/images/missing_book_cover.jpg">
                        <div class="tile_details">
                            <a href="/librarian/{{user_id}}/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                            <h4>{{book['author']}}</h4>
                            <p>{{book['available']}}</p>
                        </div>
                    </div>  
                % end
            </div>
        </div>
    </body>

</html>