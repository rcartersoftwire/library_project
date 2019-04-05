% rebase('visitor_pages/visitor_base.tpl', subtitle=book_details['title'])

<div class="book_details">
    % include('book_details', book_details=book_details)
</div>
% include('copy_book_details.tpl', copy_availability_details=copy_availability_details)
        