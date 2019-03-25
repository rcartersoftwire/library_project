% rebase('user_pages/user_base.tpl', subtitle=title)
    <div class="user_book_details">
        % include('book_details', title=title, author=author, publisher=publisher,
        %         year=year, description=description)
    </div>
    <div class="user_book_info">
        % if book_loaned == 1:
            <p>You currently have this book on loan. <br>
            Due Date: {{due_date}}
            </p>
            <ul>
                <li><a href="/user/{{user_id}}/return/{{book_id}}">Return book</a></li>
                <li><a href="/user/{{user_id}}/renew/{{book_id}}">Renew loan</a></li>
            </ul>
        % elif copies_available > 0:
            <ul>
                <li><a href="/user/{{user_id}}/borrow/{{book_id}}">Borrow book</a></li>
            </ul>
        %end
        
    </div>
    % include('copy_book_details.tpl', copies=copies,
    %         copies_available=copies_available, next_due=next_due )
        