 //nodejs
//npm install --save-dev javascript-obfuscator
//cnpm install javascript-obfuscator
//cnpm install uglify-js -g
var path = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
var fs = require('fs')
var JavaScriptObfuscator = require(path + 'javascript-obfuscator');
var str = fs.readFileSync('main.min.js', 'utf-8')
// var str = fs.readFileSync('default.thm.js', 'utf-8')
console.log('runing..')
 
var obfuscationResult = JavaScriptObfuscator.obfuscate(
    str,
    {
        compact: true,
        controlFlowFlattening: false,
        deadCodeInjection: false,
        debugProtection: false,
        debugProtectionInterval: false,
        disableConsoleOutput: false,
        identifierNamesGenerator: 'mangled',
        log: true,
        renameGlobals: true,
        rotateStringArray: true,
        selfDefending: false,
        stringArray: true,
        stringArrayEncoding: false,
        stringArrayThreshold: 0.75,
        unicodeEscapeSequence: false,
        // seed: 11,
        // deadCodeInjectionThreshold: 0.1
    }
);
var s2 = obfuscationResult.getObfuscatedCode();
fs.writeFileSync('hun_main.min.js', s2, { encoding: 'utf-8' })
// fs.writeFileSync('hun_default.thm.js', s2, { encoding: 'utf-8' })
console.log('finish')
// console.log(obfuscationResult.getObfuscatedCode());