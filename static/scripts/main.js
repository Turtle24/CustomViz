const myHeading = document.querySelector('h1');
myHeading.textContent = 'Hello world!';

let myImage = document.querySelector('img');

myImage.onclick = function() {
    let mySrc = myImage.getAttribute('src');
    if(mySrc === 'images/images/pic2.png') {
      myImage.setAttribute('src','images/pic.jpg');
    } else {
      myImage.setAttribute('src','images/pic2.png');
    }
}