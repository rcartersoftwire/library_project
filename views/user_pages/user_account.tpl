% rebase('user_pages/user_base.tpl', subtitle="My Account")
<style>
    .red {
        color: red;
    }
</style>

<div class="user_acc_container">
    <img class ="user_prof_pic" src="{{user.prof_pic}}">
    <div class="user_acc_details">
        <h2>{{user.first_name + ' ' + user.last_name}}</h2>
        <p>ID: {{user.id}}</p>
        <p>Joined Library {{user.join_date}}</p>
        % if not user.owe:
            <p>Fees payable: {{user.balance_str}}</p>
        % else:
            <p>Fees payable: <span class='red'>{{user.balance_str}}</span></p>
        % end
    </div>
    <div class="user_acc_options">
        <ul>
            <br>
            <li><a href="/user/{{user.id}}/account/edit">Edit Account Details</a></li>
        </ul>
        <ul>
            <li><a id="close_account" href="/user/{{user.id}}/account/close">Close Account</a></li>
        </ul>
        % if user.owe:
        <div class="pay_field">
            <form action="/user/{{user.id}}/account" method="post" style="display: inline;">
                £  <input type="number" id="payFees" name="payFees" value={{abs(user.balance)}} step="0.5">
                <input type="submit" value="Pay" />
            </form>
        </div>
        % end
    </div>
</div>

<script type="text/javascript" src="/static/confirm_close_account.js"></script>


<hr>
<h3><u>Current Loans</u></h3>
% if user.loan_count > 0:
    <table class="user_loans_table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Checkout Date</th>
                <th>Due Date</th>
            </tr>
        </thead>
        <tbody>
            % for loan in user.loans:
            <tr>
                <td><a href="/user/{{user.id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                <td>{{loan['author']}}</td>
                <td>{{loan['checkout_date']}}</td>
                % if not loan['late']:
                    <td>{{loan['due_date']}}</td>
                % else:
                    <td><span class="red">{{loan['due_date']}}</span></td>
                % end
            </tr>
            % end
        </tbody>
    </table>
% else:
    <p>You have no current loans</p>
% end

% if user.loan_count > 0 or user.owe is True:
    <script type="text/javascript" src="/static/settle_loans.js"></script>
% end

% if len(user.past_loans) > 0:
    <h3><u>Past Loans</u></h3>
    <table class="user_loans_table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Checkout Date</th>
                <th>Due Date</th>
                <th>Returned Date</th>
            </tr>
        </thead> 
        <tbody>
            % for loan in user.past_loans:
            <tr>
                <td><a href="/user/{{user.id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                <td>{{loan['author']}}</td>
                <td>{{loan['checkout_date']}}</td>
                % if not loan['late']:
                    <td>{{loan['due_date']}}</td>
                    <td>{{loan['returned_date']}}</td>
                % else:
                    <td><span class="red">{{loan['due_date']}}</span></td>
                    <td><span class="red">{{loan['returned_date']}}</span></td>
                % end
            </tr>
            % end
        </tbody>
    </table>
% end

