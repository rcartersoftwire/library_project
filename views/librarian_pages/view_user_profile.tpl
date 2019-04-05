% rebase('librarian_pages/librarian_base.tpl', subtitle='View User Account')
            <div class = "user_acc_container">
                <img class ="user_prof_pic" src="{{user.prof_pic}}">
                <div class="user_acc_details">
                    <h2>{{user.first_name+' '+user.last_name}}</h2>
                    <p>ID: {{user.id}}</p>
                    <p>Joined Library {{user.join_date}}</p>
                    % if not user.owe:
                        <p>Fees Owed: {{user.balance_str}}</p>
                    % else:
                        <p>Fees Owed: <span class='red'>{{user.balance_str}}</span></p>
                    % end
                    
                </div>    
            </div>
            <hr>
            <h3><u>Current Loans</u></h4>
            % if user.loan_count > 0:
            <table class="user_loans_table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Checkout Date</th>
                        <th>Due Date</th>
                    </tr>
                </thead>
                <tbody>
                    % for loan in user.loans:
                    <tr>
                        <td>{{loan['copy_id']}}</td>
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
                <p>{{user.first_name}} has no current loans</p>
            % end
            <br>
            <h3><u>Past Loans</u></h4>
            % if len(user.past_loans) > 0:
                <table class="user_loans_table">
                    <thead>
                        <tr>
                            <th>ID</th>
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
                            <td>{{loan['copy_id']}}</td>
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
            % else:
                <p>{{user.first_name}} has no past loans</p>
            % end
            
