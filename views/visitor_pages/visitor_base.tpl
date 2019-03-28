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
        <div id="left_column" class="column">
            % include('visitor_pages/visitor_header_bar.tpl')
            <div class="main_page">
                {{!base}}
            </div>
        </div>
        <div class="column" id="right_column">
            % include('visitor_pages/visitor_side_bar.tpl')
        </div>
    </body>
</html>