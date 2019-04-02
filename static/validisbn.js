function checkISBN() {
    let isbnInput =$("#isbn").val();
    let isbn = isbnInput.trim();
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
                check_digit += 3 * parseInt(isbn[i], 10);
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
        document.getElementById("add_book_button").disabled = false;

        var googleAPI = "https://www.googleapis.com/books/v1/volumes?q=" + isbn;
        $.getJSON(googleAPI, function(response) {
            if (typeof response.items === "undefined") {
                alert("No books match that ISBN.")
            } else {
                $("#divCheckISBN").html("");
                $("#title").val(response.items[0].volumeInfo.title);
                $("#author_name").val(response.items[0].volumeInfo.authors[0]);
                $("#description").html(response.items[0].volumeInfo.description);
                $("#publisher").val(response.items[0].volumeInfo.publisher);
                $("#year").val(response.items[0].volumeInfo.publishedDate);
                if (response.items[0].volumeInfo.imageLinks.thumbnail){
                    $("#divCover").html("<label for=\"cover\">Cover</label>")
                    $("#divCover").append("<input type=\"text\" id=\"cover\" value=\"" + response.items[0].volumeInfo.imageLinks.thumbnail + "\" name=\"cover\">")
                    $("#divCover").append("<img src=" + response.items[0].volumeInfo.imageLinks.thumbnail + ">")
                }else{
                    $("#divCover").html("<label for=\"cover\">Cover</label>")
                    $("#divCover").append("<input type=\"file\ id=\"cover\" name=\"cover\" accept=\"image/*\">")
                }
            }
        });


    }
}

// $(document).ready(function () {
//     $("#isbn").keyup(checkISBN);
//  });