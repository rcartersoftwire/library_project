function checkPasswordMatch() {
    var password = $("#new_password").val();
    var confirmPassword = $("#conf_password").val();
    if (password != confirmPassword){
        $("#divCheckPasswordMatch").html("<span class='red'><b>Passwords do not Match!</b></span>");
    }else{
        $("#divCheckPasswordMatch").html("<span class='green'><b>Passwords Match!</b></span>");
    }
}

$(document).ready(function () {
   $("#password, #conf_password").keyup(checkPasswordMatch);
});
