import { queueModal } from './modal.js';

//A function that checks if the browser is on ios safari and if it is it will call queueModal("Du måste lägga till denna sida på hemskärmen för att kunna använda den", "info", 5000)
//and it will show once per session.

export function checkIfIosSafari() {
    var ua = navigator.userAgent.toLowerCase();
    if (ua.indexOf('safari') != -1) {
        if (ua.indexOf('chrome') > -1) {
            return false;
        } else {
            if (ua.indexOf('iphone') > -1 || ua.indexOf('ipad') > -1) {
                return true;
            } else {
                return false;
            }
        }
    }
}

export function showAlertForIosSafari() {
    if (checkIfIosSafari() && !window.navigator.standalone) {
        if (!sessionStorage.getItem('alertShown')) {
            queueModal("ℹ Lägg till webbsidan på hemskärmen för att få notiser", "info", 5000);
            sessionStorage.setItem('alertShown', 'true');
        }
    }
}

export default showAlertForIosSafari;