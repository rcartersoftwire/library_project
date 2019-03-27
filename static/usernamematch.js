function checkUsernameMatch() {
    var username = $("#new_username").val();
    fetch('/get_username_list/'+username)
        .then(function(response){
            return response.json();
        })
        .then(function(jsonObj){
            if (jsonObj['nameTaken']){
                $("#divCheckUsername").html("<span class='red'><b>Username already being used!</b></span>");
                document.getElementById("join_button").disabled = true;
            }else{
                $("#divCheckUsername").html("<span class='green'><b>Username is valid!</b></span>");
                document.getElementById("join_button").disabled = false;
            }
        });

    if (username.length == 0){
        $("#divCheckUsername").html("<span class='green'><b>Username cannot be NULL!</b></span>");
        document.getElementById("join_button").disabled = true;
    }

}



$(document).ready(function () {
   $("#new_username").keyup(checkUsernameMatch);
});
