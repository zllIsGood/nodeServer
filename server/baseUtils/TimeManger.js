global.TimeManger = class TimeManger extends BaseClass {
    constructor() {
        super()
        this._handlers = []
    }

    /**
	 * 定时执行
	 * @param delay 执行间隔:毫秒
	 * @param repeat 执行次数, 0为无限次
	 * @param method 执行函数
	 * @param methodObj 执行函数所属对象
	 * @param onFinish 完成执行函数
	 * @param fobj 完成执行函数所属对象
	 */
    doTimer(delay, repeat, method, methodObj, onFinish = null, fobj = null) {
        for (var i in this._handlers) {
            var handler = this._handlers[i]
            if (handler.method == method) return;
        }
        repeat = repeat > 0 ? repeat : -1;
        if (repeat != Math.floor(repeat)) repeat = Math.floor(repeat);
        this.create(delay, repeat, method, methodObj, onFinish, fobj)
    }

    create(delay, repeat, method, methodObj, onFinish = null, fobj = null) {
        var id = setTimeout(TimeManger.ins().finish, delay, delay, repeat, method, methodObj, onFinish, fobj)
        this._handlers.push({
            method: method,
            methodObj: methodObj,
            id: id
        })
    }

    finish(delay, repeat, method, methodObj, onFinish = null, fobj = null) {
        method.call(methodObj)
        var self = TimeManger.ins()
        if (repeat == 0) {
            if (onFinish && fobj) onFinish.call(fobj);
            for (var i in self._handlers) {
                var handler = self._handlers[i]
                if (handler.method == method) self._handlers.splice(i, 1);
            }
            return;
        }

        var remove = true
        for (var i in self._handlers) {
            var handler = self._handlers[i]
            if (handler.method == method) {
                remove = false
            }
        }
        if(remove) return;

        if (repeat < 0) {
            setTimeout(TimeManger.ins().finish, delay, delay, repeat, method, methodObj, onFinish, fobj)
        }
        if (repeat > 0) {
            repeat--
            setTimeout(TimeManger.ins().finish, delay, delay, repeat, method, methodObj, onFinish, fobj)
        }
    }

    /**
	 * 清理
	 * @param method 要移除的函数
	 * @param methodObj 要移除的函数对应的对象
	 */
    remove(method, methodObj) {
        for (var i in this._handlers) {
            var handler = this._handlers[i]
            if (handler.method == method) {
                this._handlers.splice(i, 1);
                // clearTimeout(handler.id)
            }
        }
    }

    /**
	 * 清理
	 * @param methodObj 要移除的函数对应的对象
	 */
    removeAll(methodObj) {
        for (var i in this._handlers) {
            var handler = this._handlers[i]
            if (handler.methodObj == methodObj) {
                this._handlers.splice(i, 1);
                // clearTimeout(handler.id)
            }
        }
    }
}