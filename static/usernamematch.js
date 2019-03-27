function checkUsernameMatch() {
    var username = $("#new_username").val();
    fetch('/get_username_list/'+username)
        .then(function(response){
            return response.json();
        })
        .then(function(jsonObj){
            if (jsonObj['nameTaken']){
                $("#divCheckUsername").html("<span class='red'>Username already being used!</span>");
                document.getElementById("join_button").disabled = true;
            }else{
                $("#divCheckUsername").html("<span class='green'>Username is valid!</span>");
                document.getElementById("join_button").disabled = false;
            }
        });

    if (username.length == 0){
        $("#divCheckUsername").html("<span class='green'>Username cannot be NULL!</span>");
        document.getElementById("join_button").disabled = true;
    }

}



$(document).ready(function () {
   $("#new_username").keyup(checkUsernameMatch);
});
