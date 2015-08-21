emojione.imagePathPNG = 'http://cdn.jsdelivr.net/emojione/assets/png/';
emojione.imagePathSVG = 'http://cdn.jsdelivr.net/emojione/assets/svg/';
window.onload = function () {
    var i;
    var messages = document.getElementsByClassName('message-span');
    console.log(messages.length);
    for (i = 0; i < messages.length; i++) {
        messages[i].innerHTML = emojione.unicodeToImage(messages[i].innerHTML);
    }
    console.log('done');
}
