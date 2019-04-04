% rebase('librarian_pages/librarian_base.tpl', subtitle='View Users')
<h2>Library Users</h2>
<div class ="search_container" style="width: 60%">
    <form action="/librarian/{{user_id}}/users/search" method="POST" class="search_bar">
        <input type="search" id="search_input" name="search_query" placeholder="Search for Library User" value="{{search}}">
        <button type="submit" id="search_button">Search</button>
    </form>
    Sort By:
    <div class="grid-container" style="grid-column-template: 50% 50%; grid-padding:10%">
        <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=first_name">First Name</a>
        <a href="/librarian/{{user_id}}/users/view?search={{search}}&sort=last_name">Last Name</a>
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
            <div class="grid-container" style="grid-template-columns: 20% 80%; grid-gap:10%;">
                <div class="left-info" style="grid-column-end:1; max-width:unset; width:100%; height:100%">
                    <img class ="user_prof_pic_list" src="{{user.prof_pic}}" style="max-width: unset; width: 100%;">
                </div>
                <div class="right-info" style="padding: 0;">
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
                    <div class="loan_details">
                        % if user.loan_count > 0:
                        <table class="user_loans_table">
                            <tr>
                                <th>Title</th>
                                <th>Author</th>
                                <th>Due Date</th>
                            </tr>
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
                        </table>
                        % end
                    </div>
                </div>
            </div>
        </div>
        <hr>
    % end
</div>
<script type="text/javascript" src="/static/user_loan_detail_toggle.js"></script>
