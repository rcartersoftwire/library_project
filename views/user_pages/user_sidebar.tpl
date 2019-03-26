
<div class="side_bar">
    <div class = "user_welcome">
        <h4>Welcome {{user_first_name}}</h4>
        <p>You have {{user_loan_count}} active loans</p>
    </div>
    <div class="sidebar_links">
        <ul>
            <li><a href="/user/{{user_id}}/account">My Account</a></li>
            <li><a href="/logout">Log Out</a></li>
        </ul>
    </div>
    <div class="current_loans_summary">
        <ul>
            % for loan in user_loans:
                <li><a href="/user/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}, due {{loan['due_date']}}</a></li>
            % end
        </ul>
    </div>
    <div class="library_info">
        <h3>The Library</h3>
        <p>7 Cherry Tree Lane <br>
            Laketown
        </p>
        <p>01234 567890</p>
    </div>
</div>
       