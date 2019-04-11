
//nodejs
var mod = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
var Excel = require(mod + 'exceljs');
var workbook = new Excel.Workbook();

var fs = require('fs');
var path = require('path');//解析需要遍历的文件夹
var filePath = path.resolve('E:/game/common/trunk/config/表格导出');//需要遍历的文件夹
// var filePath = path.resolve('E:/game/common/branch/mojie/config/表格导出');//需要遍历的文件夹
var files = []
var targetFiles = {}
var string = 'GodWeaponLineConfig'   //search string
//调用文件遍历方法
fileDisplay(filePath);
//文件遍历方法
function fileDisplay(filePath) {
    //根据文件路径读取文件，返回文件列表
    var ff = fs.readdirSync(filePath)
    //遍历读取到的文件列表
    ff.forEach(function (filename) {
        //获取当前文件的绝对路径
        var filedir = path.join(filePath, filename);
        //根据文件路径获取文件信息，返回一个fs.Stats对象
        var stats = fs.statSync(filedir)
        var isFile = stats.isFile();//是文件
        var isDir = stats.isDirectory();//是文件夹
        if (isFile) {
            // if(filename.indexOf('X-新语言包配置表.xlsx') >= 0) return;
            // if (filename.indexOf('W-物品配置表.xlsx') >= 0) return files.push(filedir);
            if (filename.indexOf('~$') >= 0) return;
            if (filename.indexOf('.xlsx') >= 0) files.push(filedir);//筛选文件类型 
            // console.log(filedir);
        }
        if (isDir) {
            fileDisplay(filedir);//递归，如果是文件夹，就继续遍历该文件夹下面的文件
        }

    });
}
var len = files.length
// console.log(files);
var pos = 0
loadNext();
function loadNext() {
    var filePathName = files[pos]
    var len = files.length
    console.log(pos + 1, len, filePathName);
    workbook.xlsx.readFile(filePathName)
        .then(function () {
            var worksheets = workbook._worksheets;
            for (var j in worksheets) {
                var worksheet = worksheets[j]
                if (!worksheet) continue;
                var rows = worksheet._rows
                for (var i in rows) {
                    var cell2 = rows[i]
                    if (!cell2) continue;
                    var cells = cell2._cells
                    if (!cells) continue;
                    for (var k in cells) {
                        var cell = cells[k]
                        if (!cell) continue;
                        var value = cell.value;
                        if (typeof value == 'string') {
                            if (value.indexOf(string) >= 0)
                                targetFiles[filePathName] = filePathName + '=>address:' + cell._address;
                        }
                    }
                }
            }
            pos++;
            var len = files.length
            if (pos < len) loadNext();
            else {
                var str = JSON.stringify(targetFiles, null, '\t')
                console.log(str)
                console.warn('tips: finish') //
            }
        })
}
