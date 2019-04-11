
var fs = require('fs');
var path = require('path');//解析需要遍历的文件夹
console.warn('start..')
var str = fs.readFileSync('config.json', { encoding: 'utf8' })
var obj = JSON.parse(str)
// str = JSON.stringify(obj, null, 0) //str格式
str = JSON.stringify(obj) //str格式

var obj1 = {}, obj2 = {}, obj3 = {}, obj4 = {};

var len = str.length
var n_child = len / 4

var cur = 1
var ob;
for (var i in obj) {
    switch (cur) {
        case 1:
            ob = obj1
            break;
        case 2:
            ob = obj2
            break;
        case 3:
            ob = obj3
            break;
        case 4:
            ob = obj4
            break;
        default:
            break;
    }
    ob[i] = obj[i]

    if (JSON.stringify(ob).length >= n_child) cur++;
    cur = cur > 4 ? 4 : cur;
}


obj1 = JSON.stringify(obj1)
obj2 = JSON.stringify(obj2)
obj3 = JSON.stringify(obj3)
obj4 = JSON.stringify(obj4)

fs.writeFileSync('config1.json', obj1, 'utf-8')
fs.writeFileSync('config2.json', obj2, 'utf-8')
fs.writeFileSync('config3.json', obj3, 'utf-8')
fs.writeFileSync('config4.json', obj4, 'utf-8')
fs.writeFileSync('config-min.json', str, 'utf-8')
console.warn('finish')
