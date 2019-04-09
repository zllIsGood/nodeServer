// var GameByteArray = require('./GameByteArray')
// var BaseClass = require('./BaseClass')
// var DefaultSys = require('./DefaultSys')
// var RoleSys = require('./RoleSys')

var GameMode = []
GameMode[0] = DefaultSys;
GameMode[255] = RoleSys;

/* module.exports */global.GameLogic = class GameLogic extends BaseClass {
    
    static paser(msg, ws) {
        msg.position = 12
        var ID = msg.readUnsignedByte()
        var mod = GameMode[ID];
        if(mod)  mod.ins().paser(msg, ws);
    }
}