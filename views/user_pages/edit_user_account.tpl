% rebase('user_pages/user_base.tpl', subtitle="Edit User Account")

<h2>Edit User Account</h2>
% if defined('message'):
    <p class="flash">{{ message }}</p>
% end 
<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="/static/passwordmatch.js"></script>



  <style>
  .red {
    color: red;
  }
  .green {
      color: green;
  }
  </style>


<div class = "form">
    <form action="/user/{{user.id}}/account/edit" method="post" enctype="multipart/form-data">
    <div>
        <label for="prof_pic">Profile Picture</label>
        <input type="file" id="prof_pic" name="prof_pic" value={{user.prof_pic}} accept="image/*">
    </div>
    <div>
        <label for="first_name">First Name</label>
        <input type="text" id="first_name" name="first_name" required=required value={{user.first_name}}>
    </div>
    <div>
        <label for="last_name">Last Name</label>
        <input type="text" id="last_name" name="last_name" value={{user.last_name}}>
    </div>
    <div>
        <label for="username">Username</label>
        <input type="text" id ="new_username" name="username" value={{user.username}} required=required onfocusout="checkUsernameMatch()">                        
    </div>
    <div>
        <label for="old_password">Old Password</label>
        <input type="password" id="old_password" name="old_password">
    </div>
    <div>
        <label for="password">New Password</label>
        <input type="password" id="new_password" name="new_password">
    </div>
    <div>
        <label for="conf_password">Confirm Password</label>
        <input type="password" id="conf_password" name="conf_password" onChange="checkPasswordMatch()">
    </div>

    <div class="registrationFormAlert" id="divCheckPassword"></div>
    <div>
        <button type="submit" id="join_button">Update Account</button>
    </div>
    </form>
</div>
