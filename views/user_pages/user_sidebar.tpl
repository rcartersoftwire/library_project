
<div class="side_bar">
    <div class="sidebar_top">
        <div class = "user_welcome">
            <h4>Welcome {{user['first_name']}}</h4>
            % if user['loan_count'] == 1: 
                <p>You have {{user['loan_count']}} active loan</p>
            % else:
                <p>You have {{user['loan_count']}} active loans</p>
            % end
        </div>
        <div class="sidebar_links">
            <ul>
                <li><a href="/user/{{user['id']}}/account">My Account</a></li>
                <li><a href="/user/{{user['id']}}/book_request">Submit a Book Request</a></li>
                <li><a href="/logout">Log Out</a></li>
            </ul>
        </div>
        <div class="current_loans_summary">
            <ul>
                % for loan in user['loans']:
                    <li><a href="/user/{{user['id']}}/book/{{loan['book_id']}}">{{loan['title']}}, due {{loan['due_date']}}</a></li>
                % end
            </ul>
        </div>
    </div>
    <div class="library_info">
        <h3>The Library</h3>
        <p>7 Cherry Tree Lane <br>
            Laketown
        </p>
        <p>01234 567890</p>
    </div>
</div>
       