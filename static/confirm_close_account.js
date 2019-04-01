
function confirmAccDeletion(link){
    if (!confirm('Account will be permanently lost. Are you sure you want to close your account?')){
        link.preventDefault();
    }
}

let close_account = document.getElementById("close_account");
close_account.addEventListener("click", confirmAccDeletion);
console.log('HELLO')