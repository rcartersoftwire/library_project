<div class="side_bar">
    <div class="sidebar_top">
        <div class="login_container">
            <form action="/login" method="POST" class="login_form">
                <div>
                    <label for="username">Username</label>
                </div>
                <div>
                    <input type="text" id ="username" name="username" placeholder="Username">                      
                </div>
                <div>
                    <label for="password">Password</label>
                </div>
                <div>
                    <input type="password" id="password" name="password" placeholder="Password">
                </div>
                <br><br>
                <div class="visitor_sidebar_buttons">
                    <button type="submit" id="login_button">Log In</button>
                    <button class="signup" type="button" onclick="location.href='/join';" value="Join the library">Sign Up</button>                
                </div>
            </form>
            % if defined('message'):
            <p class="flash">{{ message }}</p>
            % end
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