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
        % include('header_bar.tpl')
        % include('visitor_pages/visitor_side_bar.tpl')
        <div class="main_page">
            {{!base}}
        </div>
    </body>
</html>