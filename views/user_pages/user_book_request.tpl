% rebase('user_pages/user_base.tpl', subtitle="Submit Book Request")

<h2>Submit a Book Request</h2>

% if defined('message'):
    <p class="flash">{{ message }}</p>
% end 
<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>

<div class = "form">
    <form action="/user/{{user['id']}}/book_request" method="post" enctype="multipart/form-data">
    <div>
        <label for="title">Title</label>
        <input type="text" id="title" name="title" required=required>
    </div>
    <div>
        <label for="author_name">Author Name</label>
        <input type="text" id="author_name" name="author_name" required=required onChange="checkAuthorName()">
    </div>
    <div>
        <button type="submit" id="add_request_button">Add</button>
    </div>
    </form>
</div>
