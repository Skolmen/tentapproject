// JavaScript to handle the fade-out animation

var modalIsShown = false;
var modalQueue = [];
const modalTypes = {
    "success": "green",
    "error": "red",
    "info": "blue",
}

window.addEventListener("load", () => {
    const modal = document.getElementById("modal");        

    modal.addEventListener("click", () => {
        hideModal()
    });
});

export function queueModal(text, type) {
    if (!modalTypes[type]) {
        console.log("Invalid modal type: " + type);
        return;
    }
    modalQueue.push([text, type]);
    if (!modalIsShown) {
        showModalFromQueue();
    }
}

function showModalFromQueue() {
    if (modalQueue.length == 0) return;
    modalIsShown = true;
    modal.style.display="block";
    modal.style.opacity=1;
    //Set color of modal depending on type
    modalInner.style.backgroundColor = modalTypes[modalQueue[0][1]];
    modalContent.innerHTML = modalQueue[0][0];
    setTimeout(() => {
        hideModal();
    }, 1500);    
}

function hideModal(){
    if (!modalIsShown) return;
    modal.style.opacity = 0; // Fade out the modal
    setTimeout(() => {
        modal.style.display = "none"; // Hide the modal
        modalContent.innerHTML = "";
        modalIsShown = false;
        modalQueue.shift();
        showModalFromQueue();
    }, 800); // Adjust the time (in milliseconds) to match the CSS transition duration
}


