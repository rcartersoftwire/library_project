% rebase('librarian_pages/librarian_base.tpl', subtitle="Edit Book")

<h2>Edit Book</h2>

% if defined('message'):
    <p class="flash">{{ message }}</p>
% end 

<div class = "form">
    <form action="/librarian/{{user_id}}/edit" method="post" enctype="multipart/form-data">
    <input type="hidden" id="book_id" name="book_id" value={{book_details['id']}}>
    <div>
        <label for="title">Title</label>
        <input type="text" id="title" name="title" required=required value="{{book_details['title']}}" readonly>
    </div>
    <div>
        <label for="author_name">Author Name</label>
        <input type="text" id="author_name" name="author_name" required=required value="{{book_details['author']}}" readonly>
    </div>
    <div>
        <label for="isbn">ISBN</label>
        <input type="text" id ="isbn" name="isbn" required=required value="{{book_details['isbn']}}" readonly>                        
    </div>
    <div>
        <label for="description">Description</label>
        <textarea id="description" name="description" value="{{book_details['description']}}">
        </textarea>
    </div>
    <div>
        <label for="publisher">Publisher</label>
        <input type="text" id="publisher" name="publisher" value="{{book_details['publisher']}}">
    </div>
    <div>
        <label for="year">Year</label>
        <input type="text" id="year" name="year" value="{{book_details['year']}}">
    </div>
    <div>
        <label for="cover">Cover</label>
        <input type="file" id="cover" name="cover" accept="image/*" value="{{book_details['cover']}}">
    </div>
    <div>
        <button type="submit" id="edit_book_button">Update</button>
    </div>
    </form>
</div>
