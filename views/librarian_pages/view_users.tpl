% rebase('librarian_pages/librarian_base.tpl', subtitle='View Users')

<h2>Library Users</h2>
<div class="users_display">
% for user in user_list:
    <div class="user_info">
        <h3>{{user['name']}}</h3>
        % if user['loan_count'] == 1:
            <h5>{{user['loan_count']}} active loan</h5>
        % else:
            <h5>{{user['loan_count']}} active loans</h5>
        % end

        % if user['loan_count'] > 0:
            <div class="user_loan_details">
                <ul>
                % for loan in user['loans']:
                    <li><a href="librarian/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}</a>, due {{loan['due_date']}}</li>
                % end
                </ul>
            </div>
        % end
    </div>
% end
</div>
