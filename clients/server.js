var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname + '/static/')).listen(8080);
