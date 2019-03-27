function checkPasswordMatch() {
    var password = $("#new_password").val();
    var confirmPassword = $("#conf_password").val();
    if (password != confirmPassword){
        $("#divCheckPassword").html("<span class='red'><b>Passwords do not Match!</b></span>");
        document.getElementById("join_button").disabled = true;
    }else{
        $("#divCheckPassword").html("<span class='green'><b>Passwords Match!</b></span>");
        document.getElementById("join_button").disabled = false;
    }
    checkPasswordLength();
}

function checkPasswordLength() {
    var password = $("#new_password").val();
    if (password.length < 8){
        $("#divCheckPassword").html("<span class='red'><b>Password needs to have at least 8 characters!</b></span>");
        document.getElementById("join_button").disabled = true;
    }
}


$(document).ready(function () {
   $("#new_password, #conf_password").keyup(checkPasswordMatch);
});
