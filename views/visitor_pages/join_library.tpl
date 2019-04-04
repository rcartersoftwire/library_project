% rebase('visitor_pages/visitor_base.tpl', subtitle="Join")

<h2>Join the Library</h2>
% if defined('message'):
    <p class="flash">{{ message }}</p>
% end 
<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="/static/passwordmatch.js"></script>
<script type="text/javascript" src="/static/usernamematch.js"></script>
<script type="text/javascript" src="/static/librariantoken.js"></script>

  <style>
  .red {
    color: red;
  }
  .green {
      color: green;
  }
  </style>


<div class = "form">
    <form action="/join" method="post" enctype="multipart/form-data">
    <div>
        <label for="prof_pic">Profile Picture</label>
        <input type="file" id="prof_pic" name="prof_pic" accept="image/*">
    </div>
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
        <input type="text" id ="new_username" name="username" required=required onKeyUp="queueCheckUsernameMatch()">                        
    </div>
    <div>
        <label for="password">Password</label>
        <input type="password" id="new_password" name="password" required=required>
    </div>
    <div>
        <label for="conf_password">Confirm Password</label>
        <input type="password" id="conf_password" name="conf_password" required=required onKeyUp="queueCheckPasswordMatch()">
    </div>
    <div>
        <label for="acc_type">Account Type</label>
        <select name = "acc_type" id="acc_type" onChange="askForToken()">
            <option value=0>Member</option>
            <option value=1>Librarian</option>
        </select>
    </div>
    <div class="librarianTokenRequest" id="divLibrarianToken"></div>
    <div class="registrationFormAlert" id="divCheckUsername"></div>
    <div class="registrationFormAlert" id="divCheckPassword"></div>
    <div>
        <button type="submit" id="join_button">Join</button>
    </div>
    </form>
</div>
