//cnpm install websocket -g
var mod = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
const WebSocket = require(mod + 'ws')
const WebSocketServer = WebSocket.Server;

require('./Globel')
var GameLogic = require('./GameLogic')

// 创建 websocket 服务器 监听在 3000 端口
const wss = new WebSocketServer({ port: 3000 })

// 服务器被客户端连接
wss.on('connection', (ws) => {
    // 通过 ws 对象，就可以获取到客户端发送过来的信息和主动推送信息给客户端

    var check = 0 //false
    // 接收客户端信息并把信息返回发送
    ws.on('message', (message) => {
        if (check == 0) {
            var key = Math.random() * (2 ^ 20)
            var bytes = new GameByteArray()
            bytes.endian = "littleEndian"
            bytes.writeUnsignedInt(key)
            ws.send(bytes._bytes)
            check++
        }
        else if (check == 1) {
            check++
        }
        else if (check == 2) {  //acount check
            var n = message.byteLength
            var msg = new GameByteArray()
            msg.endian = "littleEndian"
            for (var i = 0; i < n; i++) {
                msg.writeByte(message[i])
            }
            msg.position = 12
            var ID = msg.readUnsignedByte()
            var id = msg.readUnsignedByte()
            if (ID != 255) return;
            if (id == 1) {
                var serverid = msg.readInt()
                var acuont = msg.readString()
                var password = msg.readString()
            }

            var bytes = new GameByteArray()
            bytes.endian = "littleEndian"
            bytes.writeUnsignedShort(52462)
            bytes.position += 6
            var sysId = 255
            var msgId = 1
            bytes.writeCmd(sysId, msgId)
            // var bytes = BaseSys.ins().getBytes(255, 1)
            bytes.writeByte(0)
            ws.send(bytes._bytes, err)
            check++    //
        }
        else if (check == 3) { //game
            var n = message.byteLength
            var msg = new GameByteArray()
            msg.endian = "littleEndian"
            for (var i = 0; i < n; i++) {
                msg.writeByte(message[i])
            }

            GameLogic.paser(msg, ws) //解析
        }
    })
    ws.on('close', (coded, reason) => {
        console.log('websocket closed', coded, reason)
    })
})
