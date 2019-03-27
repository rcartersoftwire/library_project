function checkAuthorName() {
    var author = $("#author_name").val();
    var words = author.split(' ');
    let validName = true;
    if (words.length>1){
        for (let i = 0; i< words.length; i++){
            console.log(words[i].length)
            if (words[i].length == 0){
                validName = false;
                break;
            }
        }
    }else{
        validName=false;
    }

    if (!validName){
        $("#divCheckAuthor").html("<span class='red'>At least two words required for Author's Name!</span>");
        document.getElementById("add_book_button").disabled = true;
    }else{
        $("#divCheckAuthor").html("<span class='green'><b></b></span>");
        document.getElementById("add_book_button").disabled = false;
    }
}


$(document).ready(function () {
   $("#author_name").keyup(checkAuthorName);
});
