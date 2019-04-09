var ByteArray = require('./ByteArray')

/* module.exports */global.GameByteArray = class GameByteArray extends ByteArray {
    readString() {
        var s = this.readUTF();
        this.position += 1;
        return s;
    }

    writeString(string) {
        this.writeUTF(string);
        this.writeByte(0);
    }

    writeCmd(sysId, msgId) {
        this.writeByte(sysId);
        this.writeByte(msgId);
    }
}