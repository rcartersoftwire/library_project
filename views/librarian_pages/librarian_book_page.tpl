% rebase('librarian_pages/librarian_base.tpl', subtitle=book_details['title'])
<div class="librarian_book_details">
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
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_details['id']}}>
    <script type="text/javascript" src="/static/book_loan_detail.js"></script>
    <div class="loan_list" id="divLoanDetails">
    </div>
</div>
<br />
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_id}}>
    <script type="text/javascript" src="/static/book_location.js"></script>
    <div class="bookLocation" id="divBookLocation">
    </div>
</div>
        