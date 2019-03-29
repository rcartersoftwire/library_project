% rebase('librarian_pages/librarian_base.tpl', subtitle='Removing Copies')
<h2>Removing Copies of {{book_title}}</h2>
<link rel="stylesheet" type="text/css" href="/static/style/user_account.css">
<div class="copy_list">
    <div class="large_book_cover">
        <img src={{book_cover}}>
    </div>
    <h3>{{book_title}} by {{author}}</h3>
    <table class="copy_list_table">
        <tr>
            <th><u>ID</u></th>
            <th><u>Location</u></th>
            <th><u>Hire Period</u></th>
            <th><u>Checked Out?</u></th>
            <th><u>Borrower</u></th>
            <th></th>
        </tr>
        % for copy in copies:
        % if copy['checkout'] == 'Yes':
        <tr>
            <td>{{copy['id']}}</td>
            <td>{{copy['location']}}</td>
            <td>{{copy['hire_period']}}</td>
            <td>{{copy['checkout']}}</td>
            <td>{{copy['borrower']}}</td>
            <td><a class="checked_out" href="/librarian/{{user_id}}/remove/{{book_id}}/{{copy['id']}}"><span class='red'>Remove</span></a></td>
        </tr>
        % else: 
        <tr>
            <td>{{copy['id']}}</td>
            <td>{{copy['location']}}</td>
            <td>{{copy['hire_period']}}</td>
            <td>{{copy['checkout']}}</td>
            <td>{{copy['borrower']}}</td>
            <td><a href="/librarian/{{user_id}}/remove/{{book_id}}/{{copy['id']}}"><span class='red'>Remove</span></a></td>
        </tr>
        % end
        % end
    </table>
</div>
<script type="text/javascript" src="/static/confirm_copy_deletion.js"></script>
