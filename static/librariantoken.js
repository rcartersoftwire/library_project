function askForToken() {
    var acc_type = $("#acc_type").val();

    if (acc_type == 1){
        $("#divLibrarianToken").html("<div><label for=\"token\">Librarian Token</label><input type=\"token\" id=\"token\" name=\"token\" required=required></div>");
    }else{
        $("#divLibrarianToken").html("");
    }
}

