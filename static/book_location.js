var book_id = document.getElementById("book_id").value;

fetch('/get_book_location/'+book_id)
.then(function(response){
    return response.json();
})
.then(function(jsonObj){
    $("#divBookLocation").append("There are <b>" + jsonObj['downstairs'] + '</b> copy downstairs and <b>' + jsonObj['upstairs'] + '</b> copy upstairs.');
});

