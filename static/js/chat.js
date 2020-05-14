$(document).ready(function(){
    var alreadyExecuted = false;
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');

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
