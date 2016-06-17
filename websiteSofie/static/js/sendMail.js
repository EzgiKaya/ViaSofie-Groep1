function sendMail() {
    var link = "mailto:email@jordandevogelaere.be"
             + "&subject=" + escape(document.getElementById('subject').value)
             + "&body=" + escape(document.getElementById('myText').value);
console.log("test");
    window.open(link);
}
