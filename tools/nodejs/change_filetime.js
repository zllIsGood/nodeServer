//修改时间
var fs = require('fs');
var path = require('path');//解析需要遍历的文件夹
console.warn('start..')

// （1）path：文件的路径
// （2）atime：修改后的访问时间
// （3）mtime：修改后的修改时间
// （4）callback：回调函数
// fs.utimesSync('./cfg.min.json', new Date(), new Date())
fs.utimesSync('error', new Date(), new Date())

console.warn('finish')