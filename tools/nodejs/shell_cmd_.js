//nodejs 调用cmd
var process = require('child_process');

// var shell_str = 'xcopy error error2'
// var shell_str = 'copy config.json cfg.min.json'
var shell_str = 'netstat -ano'
process.exec(shell_str, function (error, stdout, stderr) {
  if (error !== null) {
    console.log('exec error: ' + error);
  }
  console.log('finish: ' + error);
});