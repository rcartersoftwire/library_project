
function confirmDeletion(link){
    if (!confirm('This copy is currently on loan. Are you sure you want to remove  it?')){
        link.preventDefault();
    }
}

let checkedOutBooks = document.getElementsByClassName("checked_out");
for (let i = 0; i < checkedOutBooks.length; i++) {
    checkedOutBooks[i].addEventListener("click", confirmDeletion);
}
