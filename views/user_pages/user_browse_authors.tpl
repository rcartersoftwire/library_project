% rebase('user_pages/user_base.tpl', subtitle="Browse Titles")
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="/user/{{user['id']}}/browse/titles">Title</a></li>
    <li><a href="/user/{{user['id']}}/browse/authors">Author</a></li>
</ul>
<div class="book_display">
    <ul>
        % for author in authors:
            <li>
                <h3>{{author['name']}}</h3>
                <div class="author_book_list">
                    <ul>
                        % for book in author['books']:
                            <li><a href="/user/{{user['id']}}/book/{{book['id']}}"><h4>{{book['title']}}</h4></a></li>
                        % end
                    </ul>
                </div>
            </li>  
        % end
    </ul>
</div>