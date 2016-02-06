//   npm install socket.io
//   curl -O https://github.com/LearnBoost/Socket.IO/raw/master/socket.io.min.js

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

server.listen(process.env.BACKEND_PORT || 3000);
var listener = io.listen(server);

listener.on('connection', function(client){
    client.on('playRequest', function(genre) {
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
});
