var book_id = document.getElementById("book_id").value;

fetch('/get_loan_list/'+book_id)
.then(function(response){
    return response.json();
})
.then(function(jsonObj){
    if (jsonObj['borrower_names'].length > 0){
        $("#divLoanDetails").append("<u><b>Current loans</b></u>");
        for (let i = 0; i<jsonObj['borrower_names'].length; i++){
            $("#divLoanDetails").append("<br />" + jsonObj['borrower_names'][i]);
            $("#divLoanDetails").append('\n');
        }
    }
});

