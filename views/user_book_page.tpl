<html>
    <head>
        <title>Library | {{title}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
        <link rel="stylesheet" type="text/css" href="/static/style/user_book_page.css">
    </head>
    <body>
            % include('user_header_bar.tpl')
            % include('user_sidebar.tpl')
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
           <div class="user_book_info">
               % if book_loaned == 1:
                    <p>You currently have this book on loan. <br>
                    Due Date: {{due_date}}
                    </p>
                    <ul>
                        <li><a href="/user/{{user_id}}/return/{{book_id}}">Return book</a></li>
                        <li><a href="/user/{{user_id}}/renew/{{book_id}}">Renew loan</a></li>
                    </ul>
                % elif copies_available > 0:
                    <ul>
                        <li><a href="/user/{{user_id}}/borrow/{{book_id}}">Borrow book</a></li>
                    </ul>
                % else:
                    <!-- <ul>
                        <li><a href="/user/{{user_id}}/reserve/{{book_id}}">Reserve book</a></li>
                    </ul> -->
                %end
               
            </div>
           % include('copy_book_details.tpl', copies=copies,
           %         copies_available=copies_available, next_due=next_due )
        </div>
    </body>

</html>