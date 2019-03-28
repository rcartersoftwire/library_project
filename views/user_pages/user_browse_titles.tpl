% rebase('user_pages/user_base.tpl', subtitle="Browse Titles")
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="/user/{{user['id']}}/browse/titles">Title</a></li>
    <li><a href="/user/{{user['id']}}/browse/authors">Author</a></li>
</ul>
<div class="book_display">
    <ul>
        % for book in books:
            <li>
                <a href="/user/{{user['id']}}/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                <h4>{{book['author']}}</h4>
                <p>{{book['available']}}</p>
            </li>  
        % end
    </ul>
</div>