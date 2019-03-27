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
        