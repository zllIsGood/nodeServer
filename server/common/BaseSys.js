
global.BaseSys = class BaseSys extends BaseClass {
    constructor() {
        super()
    }

    getBytes(sysId, msgId){
        var bytes = new GameByteArray()
        bytes.endian = "littleEndian"
        bytes.writeUnsignedShort(52462)
        bytes.position += 6
        bytes.writeCmd(sysId, msgId)
        return bytes;
    }
}