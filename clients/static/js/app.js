console.log("in node.js");
soundManager.setup({
  url: '/libs/soundmanager2/swf/',
  onready: function() {
    console.log("ionready");
    var mySound = soundManager.createSound({
      id: 'aSound',
      url: '../audio/u_got_2.mp3'
    });
    console.log('about to play');
    mySound.play();
  },
  ontimeout: function() {
    // Hrmm, SM2 could not start. Missing SWF? Flash blocked? Show an error, etc.?
  }
});
/*
function connect() {
  var socket = io.connect("http://still-beach-16458.herokuapp.com:8000");

  socket.on("connect", function () {
      console.log("Connected!");
  });
}*/
