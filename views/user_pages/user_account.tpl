% rebase('user_pages/user_base.tpl', subtitle="My Account")

            <h2>{{user_first_name}}'s Account</h2>

            <p>Joined Library {{user_join_date}}</p>
            <h3>Your Loans</h4>
            % if user_loan_count > 0:
            <table class="user_loans_table">
                <tr>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Due Date</th>
                </tr>
                % for loan in user_loans:
                <tr>
                    <td><a href="/user/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                    <td>{{loan['author']}}</td>
                    <td>{{loan['due_date']}}</td>
                </tr>
                % end
            </table>
            % else:
                <p>You have no current loans</p>
            % end

            % if len(user_past_loans) > 0:
                <h3>Your Past Loans</h4>
                <table class="user_loans_table">
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                    </tr>
                    % for loan in user_past_loans:
                    <tr>
                        <td><a href="/user/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                        <td>{{loan['author']}}</td>
                    </tr>
                    % end
                </table>
            % end

        </div>
    </body>

</html>