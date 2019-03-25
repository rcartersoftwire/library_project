<html>
    <head>
        <title>Library | {{user_first_name}} {{user_last_name}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/global.css">
        <link rel="stylesheet" type="text/css" href="/static/style/user_book_page.css">
    </head>
    <body>
            % include('user_header_bar.tpl')
            % include('user_sidebar.tpl')
        <div class="main_page">
            <h2>{{first_name}}'s Account</h2>

            <p>Joined Library DD/MM/YY</p> <!-- Need to actually add a join date column -->

            <h3>Your Loans</h4>
            <table>
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Due Date</th>
                </tr>
                % for loan in user_loans:
                <tr>
                    <td>{{loan['title']}}</td>
                    <td>{{loan['author'</td>
                </tr>
            </table>

        </div>
    </body>

</html>