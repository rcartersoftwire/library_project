userDisplay = document.getElementById("users_display");

function handlePanelClick(event){
    togglePanel(event.currentTarget);
}

function togglePanel(panel){
    if (panel.classList.contains("active")){
        collapsePanel(panel);
    }
    else {
        expandPanel(panel);
    }
}

function collapsePanel(panel){
    panel.classList.remove("active");
}
function expandPanel(panel){
    let expandedPanel = userDisplay.querySelector(".active");
    if (expandedPanel) {
        expandedPanel.classList.remove("active")
    }
    
    panel.classList.add("active")
}

let loan_panels = userDisplay.getElementsByClassName("user_info");

for (let i = 0; i < loan_panels.length; i++){
    loan_panels[i].addEventListener("click", handlePanelClick);
}

alert(loan_panels.length);