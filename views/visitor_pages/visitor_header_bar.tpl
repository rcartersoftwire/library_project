<div class="header_bar">
    <div class="logo_container"><a href="/">
        <img id='logo' src="/static/images/library_logo.png"> 
        <h1>The Library</h1>
    </a></div>
    <div class ="search_container">
        <form action="/search" method="POST" class="search_bar">
            <input type="search" id="search_input" name="search_query" placeholder="Search by Book Title or Author" value="{{search}}">
            <button type="submit" id="search_button">Search</button>
        </form>
    </div>
</div>