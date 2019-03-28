function checkISBN() {
    var isbn =$("#isbn").val();
    let validISBN = false;

    if (isbn.length == 10) {
        let check_digit = 11;
        let alt_sum = 0;

        for (let i = 0; i < 9; i++) {
            let digit = parseInt(isbn[i], 10);
            let term = (10 - i) * digit;

            alt_sum += term;
        }
        alt_sum = alt_sum % 11;
        check_digit -= alt_sum;
        check_digit = check_digit % 11;

        if (check_digit == 10 && isbn[9] === 'X'){
            validISBN = true;
        } else if (check_digit == parseInt(isbn[9])) {
            validISBN = true;
        }
    }
    else if (isbn.length == 13){
        let check_digit = 0;

        for (let i=0; i < 13; i++) {
            if (i%2 == 0) {
                check_digit += parseInt(isbn[i], 10);
            } else {
                check_digit += parseInt(isbn[i], 10);
            }
        }

        check_digit = check_digit % 10;

        if (check_digit == 0) {
            validISBN = true;
        }
    }

    if (!validISBN){
        $("#divCheckISBN").html("<span class='red'>Invalid ISBN</span>");
        document.getElementById("add_book_button").disabled = true;
    }else{
        $("#divCheckISBN").html("");
        document.getElementById("add_book_button").disabled = false;
    }
}

$(document).ready(function () {
    $("#isbn").keyup(checkISBN);
 });