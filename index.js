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

var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname + '/clients/static/')).listen(process.env.PORT || 80);

server = http.createServer(function(request, response){
    var uri = url.parse(request.url).pathname;
    var filename = path.join(process.cwd(), uri);
    fs.open(filename,"r", function(err,fd) {
        if (err) {
            response.writeHead(404, {'Content-Type':'text/plain'});
            response.end("The requested URL was not found on this server.");
        }
        fs.readFile(filename, 'binary',function(err, file){
            if (err) {
                response.writeHead(500, {'Content-Type':'text/plain'});
                response.end(err + "\n");
                return;
            }
            response.writeHead(200);
            response.write(file, 'binary');
            response.end();
        });
    });
});

server.listen(3000);
var listener = io.listen(server);
var i = 0;
var test_songs = ['Lost.mp3', 'Notorious.mp3', 'Tempest.mp3'];

listener.on('connection', function(client){
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

    sh.stdout.setEncoding('utf-8');
    sh.stdout.on('data', function(data) {
        client.send(data);
    });

    sh.stderr.setEncoding('utf-8');
    sh.stderr.on('data', function(data) {
        client.send(data);
    });
});*/


var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use('/', express.static(__dirname + '/clients'));
/*app.get('/', function(req, res){
  res.sendFile(__dirname  + '/clients/index.html');
});*/

io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(3000, function(){
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
