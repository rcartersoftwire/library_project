% rebase('librarian_pages/librarian_base.tpl', subtitle=title)
<div class="librarian_book_details">
    % include('book_details', title=title, author=author, publisher=publisher,
    %         year=year, description=description)
    <div class="librarian_book_options">
        <ul>
            <li><a href="/librarian/{{user_id}}/edit/{{book_id}}">Edit Book</a></li>
            <li><a href="/librarian/{{user_id}}/remove/{{book_id}}">Remove a Copy</a></li>
            <li id="add_copy_option">Add a Copy</li>
                <div class="add_copy_container">
                    <form class="form" action="/librarian/{{user_id}}/add_copy" method="POST">
                            <input type="hidden" name="book_id" value={{book_id}}>
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
% include('copy_book_details.tpl', copies=copies,
%         copies_available=copies_available, next_due=next_due )
