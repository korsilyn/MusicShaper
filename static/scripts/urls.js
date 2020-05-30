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
