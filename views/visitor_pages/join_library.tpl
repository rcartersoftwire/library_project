% rebase('visitor_pages/visitor_base.tpl')

<h2>Join the Library</h2>
% if defined('message'):
    <p class="flash">{{ message }}</p>
% end 
<div class = "form">
    <form action="/join" method="post">
    <div>
        <label for="first_name">First Name</label>
        <input type="text" id="first_name" name="first_name" required=required>
    </div>
    <div>
        <label for="last_name">Last Name</label>
        <input type="text" id="last_name" name="last_name">
    </div>
    <div>
        <label for="username">Username</label>
        <input type="text" id ="username" name="username" required=required>                        
    </div>
    <div>
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required=required>
    </div>
    <div>
        <label for="conf_password">Confirm Password</label>
        <input type="password" id="conf_password" name="conf_password" required=required>
    </div>
    <div>
        <button type="submit" id="join_button">Join</button>
    </div>
    </form>
</div>
