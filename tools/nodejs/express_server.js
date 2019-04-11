var modelPath = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
var express = require(modelPath + 'express');
var app = express();
 
app.use(express.static('E:/'));
 
app.get('/', function (req, res) {
   res.send('Hello World');
})
 
var server = app.listen(8099, function () {
 
  var host = server.address().address
  var port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})