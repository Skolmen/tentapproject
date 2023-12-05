document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById("edit_booking").addEventListener("click", function() {
        rotateButton("edit_booking_button");
        expandMenu("edit_booking_menu");
    });
    document.getElementById("new_booking").addEventListener("click", function() {
        rotateButton("new_booking_button");
        expandMenu("new_booking_menu");
    });
    document.getElementById("delete_booking").addEventListener("click", function() {
        rotateButton("delete_booking_button");
        expandMenu("delete_booking_menu");
    });
});

function rotateButton(id) {
    var button = document.getElementById(id);
    if (button.classList.contains("rotate_button")) {
        button.classList.remove("rotate_button");
    } else {
        button.classList.add("rotate_button");
    }
}

function expandMenu(id) {
    var menu = document.getElementById(id);
    if (menu.classList.contains("hide_menu")) {
        menu.classList.remove("hide_menu");
    } else {
        menu.classList.add("hide_menu");
    }
}

