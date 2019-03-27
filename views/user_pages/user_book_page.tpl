% rebase('user_pages/user_base.tpl', subtitle=title)
    <div class="user_book_details">
        % include('book_details', title=title, author=author, publisher=publisher,
        %         year=year, description=description)
    
        <div class="user_book_info">
            % if book_loaned == 1:
                <p>You currently have this book on loan. <br>
                Due Date: {{due_date}}
                </p>
                <ul>
                    <li><a href="/user/{{user['id']}}/return/{{book_id}}">Return book</a></li>
                    <li><a href="/user/{{user['id']}}/renew/{{book_id}}">Renew loan</a></li>
                </ul>
            % elif copies_available > 0:
                <ul>
                    <li><a href="/user/{{user['id']}}/borrow/{{book_id}}">Borrow book</a></li>
                </ul>
            %end
            
        </div>
    </div>
    % include('copy_book_details.tpl', copies=copies,
    %         copies_available=copies_available, next_due=next_due )
        
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_id}}>
    <script type="text/javascript" src="/static/book_location.js"></script>
    <div class="bookLocation" id="divBookLocation">
    </div>
</div>
        