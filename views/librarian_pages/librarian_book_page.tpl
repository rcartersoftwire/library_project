% rebase('librarian_pages/librarian_base.tpl', subtitle=title)

% include('book_details', title=title, author=author, publisher=publisher,
%         year=year, description=description)
<ul>
    <li><a href="/librarian/{{user_id}}/remove/{{id}}">Remove book</a></li>
</ul>
% include('copy_book_details.tpl', copies=copies,
%         copies_available=copies_available, next_due=next_due )
