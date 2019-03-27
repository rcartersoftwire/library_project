function checkPasswordMatch() {
    var password = $("#new_password").val();
    var confirmPassword = $("#conf_password").val();
    if (password != confirmPassword){
        $("#divCheckPassword").html("<span class='red'>Passwords do not Match!</span>");
        document.getElementById("join_button").disabled = true;
    }else{
        $("#divCheckPassword").html("<span class='green'>Passwords Match</span>");
        document.getElementById("join_button").disabled = false;
    }
    checkPasswordLength();
}

function checkPasswordLength() {
    var password = $("#new_password").val();
    if (password.length < 8){
        $("#divCheckPassword").html("<span class='red'>Password needs to have at least 8 characters!</span>");
        document.getElementById("join_button").disabled = true;
    }
}


$(document).ready(function () {
   $("#new_password, #conf_password").keyup(checkPasswordMatch);
});
