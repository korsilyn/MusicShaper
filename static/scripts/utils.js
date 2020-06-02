function groupBy(xs, key) {
    return xs.reduce(function(rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
}

String.prototype.toHHMMSS = function () {
    let sec_num = parseInt(this, 10);
    let hours   = Math.floor(sec_num / 3600);
    let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    let seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) hours   = "0" + hours;
    if (minutes < 10) minutes = "0" + minutes;
    if (seconds < 10) seconds = "0" + seconds;
    return [hours, minutes, seconds].join(':');
}

class Urls {
    static argTemplate = '0';

    /** @type {Map<string, string>} */
    static templates = new Map();

    /**
     * @param {string} name
     * @param {string} template
     */
    static registerUrl(name, template) {
        if (!Urls.templates.has(name)) {
            Urls.templates.set(name, template);
        }
    }

    /**
     * @param {Record<string, string>} urls
     */
    static registerUrls(urls) {
        for (const url in urls) {
            Urls.registerUrl(url, urls[url]);
        }
    }

    /**
     * @param {string} name
     * @param {...any} args
     */
    static reverseUrl(name, ...args) {
        let url = Urls.templates.get(name);
        if (url === undefined) {
            return console.error(`can't find url named '${name}' (Urls)`);
        }

        for (const arg of args) {
            url = url.replace(Urls.argTemplate, arg);
        }

        return url;
    }
}
