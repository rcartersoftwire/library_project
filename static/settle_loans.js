
function settleLoans(link){
    // if (!confirm('Please settle your current loans and outstanding fees before closing your account!')){
    //     link.preventDefault();
    // }
    alert('Please settle your current loans and outstanding fees before closing your account!');
}

let settleLoansWarning = document.getElementById("close_account");
settleLoansWarning.addEventListener("click", settleLoans);
