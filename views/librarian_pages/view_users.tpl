% rebase('librarian_pages/librarian_base.tpl', subtitle='View Users')
<h2>Library Users</h2>
<div class ="search_container" style="width: 60%">
    <form action="/librarian/{{user_id}}/users/search" method="POST" class="search_bar">
        <input type="search" id="search_input" name="search_query" placeholder="Search for Library User" value="{{search}}">
        <button type="submit" id="search_button">Search</button>
    </form>
    Sort By:
    <div class="grid-container" style="width: 300px; grid-column-template: 33% 33%; grid-padding:10%">
        % if order == 'DESC':
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=id&order=ASC">User ID</a>
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=first_name&order=ASC">First Name</a>
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=last_name&order=ASC">Last Name</a>
        % else:
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=id&order=DESC">User ID</a>
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=first_name&order=DESC">First Name</a>
            <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=last_name&order=DESC">Last Name</a>
        % end
    </div>
</div>
<div id="users_display">
    % if len(search) > 0:
        % if len(user_list) == 0:
            <h3>No users found with keyword "{{search}}"</h3>
        % else:
            <h3>{{len(user_list)}} user(s) found with keyword "{{search}}"</h3>
        % end 
    % end
    % for user in user_list:
        <div class="user_info">
            <div class="user_list_container">
                <img class ="user_list_prof_pic" src="{{user.prof_pic}}">
                <div class="user_list_details">
                    <p>ID: {{user.id}}</p>
                    <a href="/librarian/{{user_id}}/users/view/{{user.id}}"><h3>{{user.name}}</h3></a>
                    % if not user.owe:
                        <p>No pending fees</p>
                    % else:
                        <p>Fees Owed: <span class='red'>{{user.balance_str}}</span></p>
                    % end
                    % if user.loan_count == 1:
                        <h5 class = "loan_count">{{user.loan_count}} active loan</h5>
                    % else:
                        <h5 class="loan_count">{{user.loan_count}} active loans</h5>
                    % end        
                </div>
                <div class="loan_details">
                    % if user.loan_count > 0:
                    <table class="user_loans_table">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Author</th>
                                <th>Due Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for loan in user.loans:
                            <tr>
                                <td><a href="/librarian/{{user_id}}/book/{{loan['book_id']}}">{{loan['title']}}</a></td>
                                <td>{{loan['author']}}</td>
                                % if not loan['late']:
                                    <td>{{loan['due_date']}}</td>
                                % else:
                                    <td><span class="red">{{loan['due_date']}}</span></td>
                                % end                            
                            </tr>
                            % end
                        </tbody>
                    </table>
                    % end
                </div>
            </div>
        </div>
        <hr>
    % end
</div>
<script type="text/javascript" src="/static/user_loan_detail_toggle.js"></script>
