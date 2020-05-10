$(document).ready(function(){
    //connect to the socket server.
    //var socket = io.connect('http://127.0.0.1:5000/test');
    //var socket = io.connect('https://plantly-restful.herokuapp.com:80/test');
    var alreadyExecuted = false;
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/test');

        socket.on('connect', function() {
            socket.send('User has connected!');
            $('#log').html('NA');
            $('#log2').html('NA');
            alreadyExecuted = false;
        });


    socket.on('TempHu', function(msg) {
        console.log("Received number " + msg.temp + "and" + msg.humid);
        if(!alreadyExecuted) {
            fnShow();
            alreadyExecuted = true;
        }
        //numbers_string = '';
        temp = msg.temp.toString();
        humid = msg.humid.toString();

        $('#log').html(temp);
        $('#log2').html(humid);
    });

    //add
    // Notification
    function fnShow() {


      Notification.requestPermission(function (perm) {
        if (perm == "granted") {
          var notification = new Notification("Device is connected!" , {
            dir: "auto",
            delay:10000,
            lang: "hi",
            icon: "http://api.randomuser.me/0.2/portraits/women/31.jpg",

          });
          notification.onshow = function(){
            var self = this;
            setTimeout(function(){
              self.close();
            }, 20000);
          }
        }
      })

      Notification.requestPermission(function (perm) {
        if (perm == "granted") {
          var notification = new Notification("The information will be update on the home_page!" , {
            dir: "auto",
            delay:10000,
            lang: "hi",
            icon: "http://500px.com/graphics/pages/team/squares/diana.jpg",

          });
          notification.onshow = function(){
            var self = this;
            setTimeout(function(){
              self.close();
            }, 30000);
          }
        }
      })

    }

});


// Button
function materialize(e, button) {

  if (!e || !button) {
    console.error('Failed to materialize, you need to pass the click event and the element.');
    return;
  }

  var x = e.offsetX, y = e.offsetY,
      ink = document.createElement('div'),
      baseStyle = 'top: ' + y + 'px; left: ' + x + 'px; ',
      widthStyle = 'border-width: ' +  button.offsetWidth / 1 + 'px; ';

  function createInk() {
    ink.className = 'ink';
    ink.setAttribute('style', baseStyle);
    button.appendChild(ink);

    requestAnimationFrame(animateToWidth);
  }

  function animateToWidth() {
    ink.setAttribute('style', baseStyle + widthStyle);
  }

  function startToFade() {
    ink.setAttribute('style', baseStyle + widthStyle + 'opacity: 0;');
  }

  function removeInk() {
    button.removeChild(ink);
  }

  requestAnimationFrame(createInk);

  setTimeout(function() {
    requestAnimationFrame(startToFade);
  }, 350);

  setTimeout(function() {
    requestAnimationFrame(removeInk);
  }, 650);
}

window.onload = function() {
  var materialButtons = document.getElementsByClassName('material'),
      i, l;

  for (i = 0, l = materialButtons.length; i < l; i++) {
    materialButtons[i].addEventListener('click', function(e) {
      materialize(e, e.target);
    });
  }
}
