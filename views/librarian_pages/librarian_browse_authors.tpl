% rebase('librarian_pages/librarian_base.tpl', subtitle="Browse Authors")
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="/librarian/{{user_id}}/browse/titles">Title</a></li>
    <li><a href="/librarian/{{user_id}}/browse/authors">Author</a></li>
</ul>
<div class="book_display">
    <ul>
        % for author in authors:
            <li>
                <h3>{{author['name']}}</h3>
                <div class="author_book_list">
                    <ul>
                        % for book in author['books']:
                            <li><a href="/librarian/{{user_id}}/book/{{book['id']}}"><h4>{{book['title']}}</h4></a></li>
                        % end
                    </ul>
                </div>
            </li>  
        % end
    </ul>
</div>