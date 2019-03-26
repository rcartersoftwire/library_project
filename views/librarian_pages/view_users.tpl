% rebase('librarian_pages/librarian_base.tpl', subtitle='View Users')
<h2>Library Users</h2>
<div id="users_display">
    % for user in user_list:
        <div class="user_info">
            <h3>{{user['name']}}</h3>
            % if user['loan_count'] == 1:
            <h5 class = "loan_count">{{user['loan_count']}} active loan</h5>
            % else:
            <h5 class="loan_count">{{user['loan_count']}} active loans</h5>
            % end
            
            <div class="loan_details">
                % if user['loan_count'] > 0:
                <table class="user_loans_table">
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Due Date</th>
                    </tr>
                    % for loan in user['loans']:
                    <tr>
                        <td><a href="/librarian/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                        <td>{{loan['author']}}</td>
                        <td>{{loan['due_date']}}</td>
                    </tr>
                    % end
                </table>
                % end
            </div>
        </div>
    % end
</div>
<script type="text/javascript" src="/static/user_loan_detail_toggle.js"></script>
