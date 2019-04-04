var timeOut

function queueCheckUsernameMatch() {
    clearTimeout(timeOut)
    timeOut = setTimeout(checkUsernameMatch, 500);
}

function checkUsernameMatch() {
    var username = $("#new_username").val();
    if (username.length == 0){
        $("#divCheckUsername").html("<span class='green'>Username cannot be NULL!</span>");
        document.getElementById("join_button").disabled = true;
    } else {

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
    }
}

