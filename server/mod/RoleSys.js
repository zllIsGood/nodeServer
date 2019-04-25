/* *选择角色系统 */
global.RoleSys = class RoleSys extends BaseSys {
    constructor() {
        super()
        this.sysId = 255
    }

    paser(msg, ws) {
        var id = msg.readUnsignedByte()
        switch (id) {
            case 4:
                this.send_255_4(ws)
                break;
            case 5:
                var roleID = msg.readInt()

                this.send_255_5(ws) //

                DefaultSys.ins().send_0_2(ws) //

                DefaultSys.ins().send_0_3(ws) //

                DefaultSys.ins().send_0_4(ws) //
                break;
        }
    }
    
    send_255_4(ws) {
        var bytes = this.getBytes(255, 4)
        bytes.writeInt(211)
        bytes.writeByte(1)
        bytes.writeInt(1) //
        bytes.writeInt(211);
        bytes.writeString('zll');
        bytes.writeInt(1);
        bytes.writeInt(0);
        bytes.writeInt(1);
        bytes.writeDouble(1);
        bytes.writeInt(1);
        bytes.writeInt(1);
        ws.send(bytes._bytes, err)
    }

    send_255_5(ws) {
        var bytes = this.getBytes(255, 5)
        bytes.writeByte(1)
        ws.send(bytes._bytes, err)
    }
}