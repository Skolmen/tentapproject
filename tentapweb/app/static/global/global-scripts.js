// JavaScript to handle the fade-out animation

//var modalIsShown = false;
//
//window.addEventListener("load", () => {
//    const modal = document.getElementById("modal");        
//
//    modal.addEventListener("click", () => {
//        hideModal()
//    });
//});
//
//function showModal(text, color) {
//    if (modalIsShown) return;
//    modalIsShown = true;
//    modal.style.display="block";
//    modal.style.opacity=1;
//    modalInner.style.backgroundColor = color;
//    modalContent.innerHTML = text;
//    setTimeout(() => {
//        hideModal();
//    }, 1500);
//}
//
//function hideModal(){
//    if (!modalIsShown) return;
//    modal.style.opacity = 0; // Fade out the modal
//    setTimeout(() => {
//        modal.style.display = "none"; // Hide the modal
//        modalContent.innerHTML = "";
//        modalIsShown = false;
//    }, 800); // Adjust the time (in milliseconds) to match the CSS transition duration
//}
