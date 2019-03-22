<html>
    <head>
        <title>Library | {{search_query}}   </title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
    </head>
    <body>
            % include('librarian_header_bar.tpl')
            % include('librarian_sidebar.tpl')
        <div class="main_page">
           <p>
               Search Results for: "{{search_query}}"
           </p>
           <div class="search_results">
               <ul>
                    % for book in results:
                        <li>
                            <a href="/librarian/{{user_id}}/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                            <h4>{{book['author']}}</h4>
                            <p>{{book['available']}}</p>
                        </li>
                    % end 
               </ul>
           </div>
        </div>
    </body>

</html>