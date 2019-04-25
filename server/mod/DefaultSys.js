/* *默认系统 */
/* module.exports */ global.DefaultSys = class DefaultSys extends BaseSys {
    constructor() {
        super()
        this.sysId = 0
    }

    paser(msg, ws) {
        var id = msg.readUnsignedByte()

        switch (id) {
            case 4:

                break;
            case 5:

                break;
            case 255: //心跳包
                // ws.terminate()// ws.close() //websocket closed 断开连接
                break;
        }
    }

    send_0_2(ws) {
        var bytes = this.getBytes(0, 2)
        bytes.writeShort(1)
        bytes.writeInt(1)
        for (var i = 0; i < 4000; i++) {
            bytes.writeInt(1)
        }
        ws.send(bytes._bytes, err)
    }

    send_0_3(ws) {
        var bytes = this.getBytes(0, 3)
        bytes.writeInt(1)
        bytes.writeInt(11)
        bytes.writeShort(5)
        bytes.writeShort(5)
        bytes.writeByte(0)
        bytes.writeString('fbname')
        bytes.writeString('fbdesc')
        ws.send(bytes._bytes, err)
    }

    send_0_4(ws) {
        var bytes = this.getBytes(0, 4)
        var handle = Math.random()

        bytes.writeShort(1)
        bytes.writeDouble(handle)
        bytes.writeInt(handle)
        bytes.writeDouble(handle)
        bytes.writeInt(100)
        bytes.writeInt(105)

        bytes.writeShort(0)
        bytes.writeShort(0)

        bytes.writeString('name')
        bytes.writeInt(0) //servId
        bytes.writeByte(1)
        bytes.writeByte(0)
        bytes.writeInt(10) //lv

        /* for (var i = 0; i < 6; i++) {
            bytes.writeInt(101001) 121001
        } */
        bytes.writeInt(121001)
        bytes.writeInt(101001)
        bytes.writeInt(1)
        bytes.writeInt(1)
        bytes.writeInt(1)
        bytes.writeInt(1)

        bytes.writeString('zll')
        for (var i = 0; i < 206; i++) {
            bytes.writeInt(0)
        }

        ws.send(bytes._bytes, err)
    }
}