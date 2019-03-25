<html>
    <head>
        <title>Library 
            % if defined('subtitle'):
            | {{subtitle}}
            % end
        </title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
    </head>
    <body>
        % include('librarian_pages/librarian_header_bar.tpl')
        % include('librarian_pages/librarian_sidebar.tpl')
        <div class="main_page">
            {{!base}}
        </div>
    </body>

</html>