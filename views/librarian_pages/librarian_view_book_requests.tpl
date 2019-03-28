% rebase('librarian_pages/librarian_base.tpl', subtitle='View Book Requests')
<h2>Book Requests</h2>
<link rel="stylesheet" type="text/css" href="/static/style/user_account.css">
<div class="book_requests">
    <table class="book_requests_table">
        <tr>
            <th><u>Title</u></th>
            <th><u>Author</u></th>
            <th></th>
        </tr>
        % for i in range(len(book_title)):
        <tr>
            <td>{{book_title[i]}}</td>
            <td>{{book_author[i]}}</td>
            <td><a href="/librarian/{{user_id}}/book_request/remove/{{req_id[i]}}"><span class='red'>Remove</span></a></td>
        </tr>
        % end
    </table>
</div>
