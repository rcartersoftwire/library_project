% rebase('librarian_pages/librarian_base.tpl', subtitle="Browse Authors")
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="/librarian/{{user_id}}/browse/titles">Title</a></li>
    <li><a href="/librarian/{{user_id}}/browse/authors">Author</a></li>
</ul>
<div class="book_display">
    <ul>
        % for book in books:
            <li>
                <a href="/librarian/{{user_id}}/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                <h4>{{book['author']}}</h4>
                <p>{{book['available']}}</p>
            </li>  
        % end
    </ul>
</div>