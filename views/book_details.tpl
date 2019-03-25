<div class="large_book_cover">
    <img src={{cover}}>
</div>
<div class="book_details">
    <h2>{{title}}</h2>
    <h3>{{author}}</h3>
    % if publisher is not None:
        <h5>{{publisher}}</h5> 
    % end
    % if year is not None:
        <h5>{{year}}</h5>
    % end
    % if description is not None:
        <p>{{description}}</p>
    % end
    <p>ISBN: {{isbn}}</p>
</div>