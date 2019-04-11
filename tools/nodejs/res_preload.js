//egret  resource >>>  res >>> RES 

function res_load(res, url) {
    var config = res.config
    var type
    var r = config.getResource(url);
    if (!r) {
        if (!type) {
            type = config.__temp__get__type__via__url(url);
        }
        r = { name: url, url, type, root: '', extra: 1 };
        config.addResourceData(r);
        r = config.getResource(url);
        if (!r) {
            throw 'never';
        }
    }

    var queue = res.queue
    queue.failedList.unshift(r)
    queue.loadNextResource()
}

function res_add(res, url) {
    var config = res.config
    var type
    var r = config.getResource(url);
    if (!r) {
        if (!type) {
            type = config.__temp__get__type__via__url(url);
        }
        r = { name: url, url, type, root: '', extra: 1 };
        config.addResourceData(r);
        r = config.getResource(url);
        if (!r) {
            throw 'never';
        }
    }

    var queue = res.queue
    queue.failedList.unshift(r)
}