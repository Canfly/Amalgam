// prototype
// Canfly © 2018
import config from './config'

const {debug} = config


var fs = require('fs');

var AMPATH = '/.am';

fs.readdir(AMPATH, function(err, items) {
  var i = 0, j = items.length;
  for(;i<j;i++) {
    var item = items[i];
    // Do something with item here

  }
});