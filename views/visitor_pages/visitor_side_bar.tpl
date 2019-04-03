<div class="side_bar">
    <div class="sidebar_top">
        <div class="login_container">
            <form action="/login" method="POST" class="login_form">
                <div>
                    <label for="username" style="width: 20%">Username</label>
                    <input type="text" id ="username" name="username">                      
                </div>
                <div>
                    <label for="password" style="width: 20%">Password</label>
                    <input type="password" id="password" name="password">
                </div>
                <div>
                    <button type="submit" id="login_button">Log In</button>
                </div>
            </form>
            % if defined('message'):
            <p class="flash">{{ message }}</p>
            % end
        </div>
        <div class="sidebar_links">
            <ul>
                <li><a href="/join">Join the Library</a></li>
            </ul>
        </div>
    </div>
    <div class="library_info">
        <h3>The Library</h3>
        <p>7 Cherry Tree Lane <br>
            Laketown
        </p>
        <p>01234 567890</p>
    </div>
</div>