<html>
        <head>
            <title>Library </title>
            <link rel="stylesheet" type="text/css" href="/static/style/global.css">
            <link rel="stylesheet" type="text/css" href="/static/style/forms.css">
        </head>
    <body>
        % include('librarian_header_bar.tpl')
        % include('librarian_sidebar.tpl')
        <div class="main_page">
            <h2>Add Book</h2>
            % if defined('message'):
              <p class="flash">{{ message }}</p>
            % end 
            <div class = "form">
                <form action="/librarian/{{user_id}}/add" method="post">
                <div>
                    <label for="title">Title</label>
                    <input type="text" id="title" name="title" required=required>
                </div>
                <div>
                    <label for="author_name">Author Name</label>
                    <input type="text" id="author_name" name="author_name" required=required>
                </div>
                <div>
                    <label for="isbn">ISBN</label>
                    <input type="text" id ="isbn" name="isbn" required=required>                        
                </div>
                <div>
                    <label for="description">Description</label>
                    <textarea id="description" name="description">
                    </textarea>
                </div>
                <div>
                    <label for="publisher">Publisher</label>
                    <input type="text" id="publisher" name="publisher">
                </div>
                <div>
                    <label for="year">Year</label>
                    <input type="text" id="year" name="year">
                </div>
                <div>
                    <label for="hire_period">Hire Period (days)</label>
                    <input type="number" id="hire_period" name="hire_period" min="1" max="21">
                </div>
                <div>
                    <label for="location">Location</label>
                    <select name = "location">
                        <option value=1>Downstairs</option>
                        <option value=2>Upstairs</option>
                    </select>
                </div>
                <div>
                    <button type="submit" id="add_book_button">Add</button>
                </div>
                </form>
            </div>
        </div>
    </body>

</html>