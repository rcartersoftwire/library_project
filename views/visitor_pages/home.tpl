% rebase('visitor_pages/visitor_base.tpl', subtitle="Join")
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="/browse_title">Title</a></li>
    <li><a href="/browse_author">Author</a></li>
    <li><a href="/browse_genre">Genre</a></li>
</ul>
<div class="book_display">
    % for book in books:
        <div class="book_tile">
            % if book['cover']:
                <img class ="book_cover" src="{{book['cover']}}">
            % else:
                <img class="book_cover" src="/static/images/missing_book_cover.jpg">
            % end    
            <div class="tile_details">
                <a href="/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                <h4>{{book['author']}}</h4>
                <p>{{book['available']}}</p>
            </div>
        </div>  
    % end
</div>