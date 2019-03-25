<p>
    Search Results for: "{{search_query}}"
</p>
<div class="search_results">
    <ul>
        % for book in results:
            <li>
                <a href="/book/{{book['id']}}"><h3>{{book['title']}}</h3></a>
                <h4>{{book['author']}}</h4>
                <p>{{book['available']}}</p>
            </li>
        % end 
    </ul>
</div>