% rebase('user_pages/user_base')
<ul class="browse_filters">
    <li>Browse by:</li>
    <li><a href="browse/titles">Title</a></li>
    <li><a href="browse/authors">Author</a></li>
</ul>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/vast-engineering/jquery-popup-overlay@2/jquery.popupoverlay.min.js"></script>
<div class="book_display">
    % for book in books:
        <div class="book_tile">
            % if book['cover']:
                <img class ="book_cover" src="{{book['cover']}}">
            % else:
                <img class="book_cover" src="/static/images/missing_book_cover.jpg">
            % end    
            <div class="tile_details">
                <a href="/user/{{user.id}}/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                <h4>{{book['author']}}</h4>
                <p>{{book['available']}}</p>
            </div>
        </div>  
    % end
</div>
% if book_requested is True:
<div id="myModal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="close">&times;</span>
    <p>Book has been requested</p>
  </div>

</div>
<script type="text/javascript" src="/static/book_requested.js"></script>

% end
