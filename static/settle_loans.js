
function settleLoans(link){
    alert('Please settle your current loans and outstanding fees before closing your account!');
    link.preventDefault();
}

let settleLoansWarning = document.getElementById("close_account");
settleLoansWarning.addEventListener("click", settleLoans);
