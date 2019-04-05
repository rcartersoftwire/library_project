% rebase('user_pages/user_base.tpl', subtitle=book_details['title'])
    <div class="book_details_container">

        <div class="book_details">
            % include('book_details', book_details=book_details)
        </div>
        <div class="librarian_book_options">
            % if book_loaned == 1:
                <p>You currently have this book on loan. <br>
                Due Date: {{due_date}}
                </p>
                <ul>
                    <li><a href="/user/{{user.id}}/return/{{book_details['id']}}">Return book</a></li>
                    <li><a href="/user/{{user.id}}/renew/{{book_details['id']}}">Renew loan</a></li>
                </ul>
            % elif copy_availability_details['num_available'] > 0:
                % if user.owe:
                    <ul>
                        <span class="red">Please settle your late payments before borrowing another book</span>
                    </ul>
                % else:
                    <ul>
                        <li><a href="/user/{{user.id}}/borrow/{{book_details['id']}}">Borrow book</a></li>
                    </ul>
                %end
            %end
            
        </div>

    </div>
    % include('copy_book_details.tpl', copy_availability_details=copy_availability_details)
        
<div>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <input type="hidden" id="book_id" value={{book_details['id']}}>
    <script type="text/javascript" src="/static/book_location.js"></script>
    <div class="bookLocation" id="divBookLocation">
    </div>
</div>
        