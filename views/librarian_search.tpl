<html>
    <head>
        <title>Library | {{search_query}}   </title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
    </head>
    <body>
            % include('librarian_header_bar.tpl')
            % include('librarian_sidebar.tpl')
        <div class="main_page">
            % include('search_results.tpl', search_query=search_query, results=results)
        </div>
    </body>

</html>