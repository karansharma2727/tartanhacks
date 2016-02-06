//   npm install socket.io
//   curl -O https://github.com/LearnBoost/Socket.IO/raw/master/socket.io.min.js
/*
var http  = require('http'),
    url   = require('url'),
    path  = require('path'),
    fs    = require('fs'),
    io    = require('socket.io'),
    sys   = require('sys'),
    util  = require('util'),
    exec = require('child_process').exec;
*/

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var multer   =  require( 'multer' );

app.use('/', express.static(__dirname + '/clients'));
app.use('/mp3modulation', express.static(__dirname + '/mp3modulation'));

var storage = multer.diskStorage({
  destination: __dirname + '/mp3modulation/music/',
  filename: function (req, file, cb) {
      cb(null, file.originalname)
  }
});

var upload = multer( { storage: storage,
                     }
                   );

app.post('/upload', upload.single( 'file' ), function(req, res, next) {
  return res.status( 200 ).send( req.file );
})


var i = 0;
var test_songs = ['Lost.mp3', 'Notorious.mp3', 'Tempest.mp3'];

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('playRequest', function(genre){
      var title = test_songs[i % test_songs.length];
      io.emit('playRequest', './mp3modulation/music/deep_house/' + title);
      console.log("trying to send user " + title);
      i++;
      return;
      /*var child = exec("python ~/combiner.py " + genre,
                       function(error, stdout, stderr){
                           if (error != NULL) {
                               io.send(stdout);
                           } else {
                               client.send("Try again later!");
                           }
                       });*/
    io.emit('chat message', msg);
  });
});

http.listen(process.env.PORT || 3000, function(){
  console.log('listening on *:3000');
});
/*
socket.on('connection', function(client){
    client.on('playRequest', function(genre) {
      if(genre === "Karan") {
        var title = test_songs[i % test_songs.length];
        client.send('http://limitless-shore-68930.herokuapp.com/mp3modulation/music/deep_house/' + title);
        i++;
        return;
      }
        var child = exec("python ~/combiner.py " + genre,
                         function(error, stdout, stderr){
                             if (error != NULL) {
                                 client.send(stdout);
                             } else {
                                 client.send("Try again later!");
                             }
                         });
    });
*/
