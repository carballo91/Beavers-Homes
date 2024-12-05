document.addEventListener('DOMContentLoaded', function(){
    let contact_message = document.getElementById("message");
    if (contact_message != null){
        setTimeout(function(){
            contact_message.style.display = "none";
        },4000);
    } 
});