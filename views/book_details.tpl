<img class="large_book_cover" src={{book_details['cover']}}>
<div class="book_info">
    <h2>{{book_details['title']}}</h2>
    <h3>{{book_details['author']}}</h3>
    % if book_details['publisher'] is not None:
        <h5>{{book_details['publisher']}}</h5> 
    % end
    % if book_details['year'] is not None:
        <h5>{{book_details['year']}}</h5>
    % end
    % if book_details['description'] is not None:
        <p>{{book_details['description']}}</p>
    % end
    <p>ISBN: {{book_details['isbn']}}</p>
</div>