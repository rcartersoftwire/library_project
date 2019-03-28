% rebase('librarian_pages/librarian_base.tpl', subtitle='View User Account')
            <img class ="user_prof_pic" src="{{user['prof_pic']}}">
            <h2>{{user['first_name']}}'s Account</h2>

            <p>Joined Library {{user['join_date']}}</p>
            <h3><u>Current Loans</u></h4>
            % if user['loan_count'] > 0:
            <table class="user_loans_table">
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Checkout Date</th>
                    <th>Due Date</th>
                </tr>
                % for loan in user['loans']:
                <tr>
                    <td><a href="/user/{{user['id']}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                    <td>{{loan['author']}}</td>
                    <td>{{loan['checkout_date']}}</td>
                    <td>{{loan['due_date']}}</td>
                </tr>
                % end
            </table>
            % else:
                <p>{{user['first_name']}} has no current loans</p>
            % end

            % if len(user['past_loans']) > 0:
                <h3><u>Past Loans</u></h4>
                <table class="user_loans_table">
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Checkout Date</th>
                        <th>Returned Date</th>
                    </tr>
                    % for loan in user['past_loans']:
                    <tr>
                        <td><a href="/user/{{user['id']}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                        <td>{{loan['author']}}</td>
                        <td>{{loan['checkout_date']}}</td>
                        <td>{{loan['returned_date']}}</td>
                    </tr>
                    % end
                </table>
            % end

        </div>
    </body>

</html>