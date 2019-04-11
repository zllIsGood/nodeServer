//cnpm install uglify-js -g
var mod = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
var UglifyJS = require(mod + 'uglify-js')
var fs = require('fs');
console.log('start..');

// var code = {
//     "file1.js": "function add(first, second) { return first + second; }",
//     "file2.js": "console.log(add(1 + 2, 3 + 4));"
// };
// var dir = 'E:/game/code/client/1.9.0/bin-release/web/1/'
var dir = 'E:/p4/code/client/trunk/bin-release/web/1/'
var sources = [
    "libs/modules/egret/egret.min.js",
    "libs/modules/egret/egret.web.min.js",
    "libs/modules/eui/eui.min.js",
    "libs/modules/assetsmanager/assetsmanager.min.js",
    "libs/modules/tween/tween.min.js",
    "libs/modules/promise/promise.min.js",
    "libs/modules/game/game.min.js",
    "libs/modules/socket/socket.min.js",
    "3rdlib/jszip/jszip.min.js",
    "3rdlib/particle/particle.min.js",
    "resource/default.thm.js",
]
var code = ''
for (var i in sources) {
    code += fs.readFileSync(dir + sources[i])
}
var result = UglifyJS.minify(code);
console.log(result.code.length);
fs.writeFileSync(dir + 'mergedv1.js', result.code)
console.log('finish');