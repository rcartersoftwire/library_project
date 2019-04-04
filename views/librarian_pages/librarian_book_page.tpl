% rebase('librarian_pages/librarian_base.tpl', subtitle=book_details['title'])
<div class="librarian_book_details">
    % if defined('message'):
        <p class="flash">{{ message }}</p>
    % end
    % include('book_details', book_details=book_details)
    <div class="librarian_book_options">
        <ul>
            <li><a href="/librarian/{{user_id}}/edit/{{book_details['id']}}">Edit Book</a></li>
            <li><a href="/librarian/{{user_id}}/remove/{{book_details['id']}}">Remove a Copy</a></li>
            <li id="add_copy_option">Add a Copy</li>
                <div class="add_copy_container">
                    <form class="form" action="/librarian/{{user_id}}/add_copy" method="POST">
                            <input type="hidden" name="book_id" value={{book_details['id']}}>
                            <div>
                                <label for="hire_period">Hire Period (days)</label>
                                <input type="number" id="hire_period" name="hire_period" value="14" required=required min="1" max="21">
                            </div>
                            <div>
                                <label for="num_of_copies">Quantity to Add</label>
                                <input type="number" id="num_of_copies" name="num_of_copies" value="1" required=required min="0">
                            </div>
                            <div>
                                <label for="location">Location</label>
                                <select name = "location">
                                    <option value=1>Downstairs</option>
                                    <option value=2>Upstairs</option>
                                </select>
                            </div>
                            <div>
                                <button type="submit" id="add_copy_button">Add</button>
                            </div>
                    </form>
                </div>
        </ul>
    </div>
    <script type="text/javascript" src="/static/add_copy_toggle.js"></script>
</div>
% include('copy_book_details.tpl', copy_availability_details=copy_availability_details)

<div class="current_loans">
    % if len(loan_list) > 0:
        <h3><u>Current Loans</u></h3>
        % for user in loan_list:
            <li><a href="/librarian/{{user_id}}/users/view/{{user[0]}}">{{user[1]}}</a></li>
        % end
    % end
</div>
<br />
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_details['id']}}>
    <script type="text/javascript" src="/static/book_location.js"></script>
    <div class="bookLocation" id="divBookLocation">
    </div>
</div>

<h3><u>Book Loan History</u></h4>
<div>
    % if loan_history == []:
        <h3>There are no loan records of this book.</h3>
    % else:
        <table class="book_loans_table">
            <tr>
                <th>ID</th>
                <th>User</th>
                <th>Checkout Date</th>
                <th>Due Date</th>
                <th>Returned</th>
                <th>Returned Date</th>
            </tr>
            % for loan in loan_history:
            <tr>
                <td>{{loan['id']}}</td>
                <td>{{loan['first_name'] + ' ' + loan['last_name']}}</td>
                <td>{{loan['checkout_date']}}</td>
                <td>{{loan['due_date']}}</td>
                <td>{{'Yes' if loan['returned'] == 1 else 'No'}}</td>
                <td>{{loan['returned_date']}}</td>

            </tr>
            % end
        </table>
    % end
</div>
