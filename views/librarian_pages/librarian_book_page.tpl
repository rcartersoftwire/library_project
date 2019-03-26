% rebase('librarian_pages/librarian_base.tpl', subtitle=title)
<div class="librarian_book_details">
    % include('book_details', title=title, author=author, publisher=publisher,
    %         year=year, description=description)
    <div class="librarian_book_options">
        <ul>
            <li><a href="/librarian/{{user_id}}/edit/{{book_id}}">Edit Book</a></li>
            <li><a href="/librarian/{{user_id}}/remove/{{book_id}}">Remove Book</a></li>
            <li><a href="/librarian/{{user_id}}/add_copy/{{book_id}}">Add a Copy</a></li>
        </ul>
    </div>
</div>
% include('copy_book_details.tpl', copies=copies,
%         copies_available=copies_available, next_due=next_due )
