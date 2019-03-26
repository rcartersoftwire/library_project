function toggleCopyForm(event){
    if (add_copy_container.classList.contains("active")){
        add_copy_container.classList.remove("active")
    }
    else{
        add_copy_container.classList.add("active")
    }
}


add_copy_option = document.getElementById("add_copy_option")
add_copy_container = document.getElementsByClassName("add_copy_container")[0]

add_copy_option.addEventListener("click", toggleCopyForm);
