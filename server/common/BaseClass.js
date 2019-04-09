/**
 * Created by yangsong on 14/12/18.
 * 基类
 */
/* module.exports */global.BaseClass =  class BaseClass {
    constructor() {

    }

	/**
	 * 获取一个单例
	 * @returns {any}
	 */
    static ins(...args) {
        let Class = this;
        if (!Class._instance) {
            Class._instance = new Class(...args);

        }
        return Class._instance;
    }

    static del() {
        let Class = this;
        if (Class._instance) {
            Class._instance = null;
        }
    }
}