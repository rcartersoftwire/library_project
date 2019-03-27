% rebase('user_pages/user_base.tpl', subtitle=book_details['title'])
    <div class="user_book_details">
        % include('book_details', book_details=book_details)
    
        <div class="user_book_info">
            % if book_loaned == 1:
                <p>You currently have this book on loan. <br>
                Due Date: {{due_date}}
                </p>
                <ul>
                    <li><a href="/user/{{user_id}}/return/{{book_details['id']}}">Return book</a></li>
                    <li><a href="/user/{{user_id}}/renew/{{book_details['id']}}">Renew loan</a></li>
                </ul>
            % elif copy_availability_details['num_available'] > 0:
                <ul>
                    <li><a href="/user/{{user_id}}/borrow/{{book_details['id']}}">Borrow book</a></li>
                </ul>
            %end
            
        </div>
    </div>
    % include('copy_book_details.tpl', copy_availability_details=copy_availability_details)
        
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_id}}>
    <script type="text/javascript" src="/static/book_location.js"></script>
    <div class="bookLocation" id="divBookLocation">
    </div>
</div>
        