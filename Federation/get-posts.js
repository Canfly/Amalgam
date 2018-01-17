// prototype
// Canfly © 2018

var https = require('https');

var options = {
  host: 'canfly.org',
  path: '/p/'
};


var req = https.request(options, function(res) {
  //console.log('STATUS: ' + res.statusCode);
  //console.log('HEADERS: ' + JSON.stringify(res.headers));
  res.setEncoding('utf8');
  res.on('data', function (chunk) {
    console.log(JSON.stringify(chunk));
  });
});

req.on('error', function(e) {
  console.log('problem with request: ' + e.message);
});

req.write('data\n');
req.write('data\n');
req.end();
