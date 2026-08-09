if (!Array.prototype.pushUnique) {
    Array.prototype.pushUnique = function (item) {
        if (!this.includes(item)) {
            this.push(item);
            return true;
        }
        return false;
    };
}
if (!Set.prototype.toggle) {
    Set.prototype.toggle = function (value) {
        if (this.has(value)) {
            this.delete(value);
            return false;
        }
        else {
            this.add(value);
            return true;
        }
    };
}
class Cookie {
    static set(name, value, days = 36500) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
    }
    static get(name) {
        const nameEQ = `${name}=`;
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i].trim();
            if (c.indexOf(nameEQ) === 0)
                return decodeURIComponent(c.substring(nameEQ.length, c.length));
        }
        return null;
    }
    static setJSON(name, data, days) {
        Cookie.set(name, JSON.stringify(data), days);
    }
    static getJSON(name) {
        const raw = Cookie.get(name);
        if (!raw)
            return null;
        try {
            return JSON.parse(raw);
        }
        catch {
            return null;
        }
    }
    static setList(name, value) {
        Cookie.setJSON(name, value);
    }
    static getList(name) {
        return Cookie.getJSON(name) ?? [];
    }
    static getSet(name, default_value = []) {
        const arr = this.getJSON(name);
        return new Set(Array.isArray(arr) && arr.length > 0 ? arr : default_value);
    }
    static setSet(name, data, days) {
        this.setJSON(name, Array.from(data), days);
    }
    static setString(name, value) {
        Cookie.set(name, value);
    }
    static getString(name) {
        return Cookie.get(name) ?? "";
    }
    static setBool(name, value) {
        Cookie.set(name, value ? '1' : '0');
    }
    static getBool(name) {
        return Cookie.get(name) === '1';
    }
    static getBtnString(name) {
        return Cookie.get(name) ?? "";
    }
    static setBtnString(name, value) {
        Cookie.set(name, value);
    }
}
class MyArray {
    static deepClone(arr) {
        return arr.map(item => Array.isArray(item)
            ? MyArray.deepClone(item)
            : item);
    }
    static occurrence(arr, value) {
        return arr.filter(v => v === value).length;
    }
    static hasDuplicates(arr) {
        return new Set(arr).size !== arr.length;
    }
    static equals(a, b) {
        return (a.length === b.length &&
            a.every((v, i) => v === b[i]));
    }
}
class MyObject {
    static deepCopy(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }
        if (Array.isArray(obj)) {
            return obj.map(item => MyObject.deepCopy(item));
        }
        const copy = {};
        for (const key in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, key)) {
                copy[key] = MyObject.deepCopy(obj[key]);
            }
        }
        return copy;
    }
    static isEmpty(obj = {}) {
        return Object.keys(obj).length === 0;
    }
    static objectsEqual(a, b) {
        const ka = Object.keys(a), kb = Object.keys(b);
        if (ka.length !== kb.length)
            return false;
        return ka.every(k => a[k] === b[k]);
    }
    static hashObjectFast(obj) {
        const FNV_PRIME = 0x01000193;
        let hash = 0x811c9dc5;
        function mixBytes(bytes) {
            for (let b of bytes) {
                hash ^= b;
                hash = Math.imul(hash, FNV_PRIME) >>> 0;
            }
        }
        function walk(value) {
            if (value === null) {
                mixBytes(new Uint8Array([0x00]));
            }
            else if (typeof value === "boolean") {
                mixBytes(new Uint8Array([value ? 0x01 : 0x02]));
            }
            else if (typeof value === "number") {
                const buf = new ArrayBuffer(8);
                new DataView(buf).setFloat64(0, value, true);
                mixBytes(new Uint8Array(buf));
            }
            else if (typeof value === "string") {
                mixBytes(new TextEncoder().encode(value));
                mixBytes(new Uint8Array([0x00]));
            }
            else if (Array.isArray(value)) {
                mixBytes(new Uint8Array([0xF0]));
                for (let el of value)
                    walk(el);
                mixBytes(new Uint8Array([0xF1]));
            }
            else if (typeof value === "object") {
                mixBytes(new Uint8Array([0xE0]));
                const keys = Object.keys(value).sort();
                for (let key of keys) {
                    mixBytes(new TextEncoder().encode(key));
                    mixBytes(new Uint8Array([0x00]));
                    walk(value[key]);
                }
                mixBytes(new Uint8Array([0xE1]));
            }
            else {
                mixBytes(new Uint8Array([0xFF]));
            }
        }
        walk(obj);
        return hash.toString(16);
    }
}
class Loader {
    static loadJSAsync(src) {
        if (!src.endsWith('.js')) {
            throw new Error(`Not a JS file: ${src}`);
        }
        if (!/^https?:\/\//i.test(src)) {
            src = src.slice(0, -3);
        }
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = src;
            script.onload = () => resolve();
            script.onerror = () => reject(new Error(`Failed to load ${src}`));
            document.head.appendChild(script);
        });
    }
    static loadJS(src, callback) {
        if (!src.endsWith('.js')) {
            throw new Error(`Not a JS file: ${src}`);
        }
        src = src.slice(0, -3);
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = src;
        script.onload = () => callback?.();
        document.head.appendChild(script);
    }
    static loadCSS(href) {
        if (!href.endsWith('.css')) {
            throw new Error(`Not a CSS file: ${href}`);
        }
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = href;
        document.head.appendChild(link);
    }
    static loadFile(filename, callback) {
        if (filename.endsWith('.js')) {
            return callback
                ? Loader.loadJS(filename, callback)
                : Loader.loadJSAsync(filename);
        }
        else if (filename.endsWith('.css')) {
            Loader.loadCSS(filename);
        }
        else {
            throw new Error(`Unsupported file type: ${filename}`);
        }
    }
}
class Client {
    static getOffsetClient(el) {
        if (el == null) {
            Lib.alert();
        }
        const rect = el.getBoundingClientRect();
        const scrollX = window.scrollX;
        const scrollY = window.scrollY;
        return {
            left: rect.left + scrollX,
            top: rect.top + scrollY,
            right: rect.right + scrollX,
            bottom: rect.bottom + scrollY,
            width: rect.width,
            height: rect.height,
        };
    }
    static getOffset(el) {
        let x = el.style.getPropertyValue('--x');
        if (x) {
            let y = el.style.getPropertyValue('--y');
            let tx = Number(x);
            let ty = Number(y);
            return {
                left: tx,
                top: ty,
            };
        }
        else {
            return {
                left: 0,
                top: 0
            };
        }
    }
    static getOffset2(elx) {
        return Client.getOffset(elx);
    }
}
class MyString {
    static isNumeric(str) {
        return !isNaN(parseFloat(str));
    }
    static insertHyphens(input) {
        return input.split('').map((char, index) => {
            if (char === char.toUpperCase() && index !== 0) {
                return '-' + char;
            }
            return char;
        }).join('').toLocaleLowerCase();
    }
    static isStringANumber(value) {
        return !isNaN(parseFloat(value)) && isFinite(Number(value));
    }
}
class Game {
    static removeTypeClasses(divElement) {
        if (divElement) {
            const classList = divElement.classList;
            const classesToRemove = [];
            classList.forEach((className) => {
                if (className.startsWith('type-')) {
                    classesToRemove.push(className);
                }
            });
            classesToRemove.forEach((className) => {
                divElement.classList.remove(className);
            });
        }
    }
    static addTypeClass(divElement, class_name, name = "") {
        divElement.classList.add(`type-${Lib.string.insertHyphens(class_name)}`);
        if (name && class_name == "StatusCard") {
            divElement.classList.add(`type-${Lib.string.insertHyphens(class_name + name)}`);
        }
    }
    static cleanResText(input) {
        const cardTypes = ["mental", "physical", "energy", "wild", 'boost'];
        cardTypes.forEach(c => {
            input = input.replaceAll(`[[${c}]]`, `<span class='icon-${c}'></span>`);
            input = input.replaceAll(`[${c}]`, `<span class='icon-${c}'></span>`);
        });
        return input;
    }
}
export class Lib {
    static getCallerFunctionName(level = 1) {
        function getErrorObject() {
            return new Error('');
        }
        try {
            const err = getErrorObject();
            const callerLine = err.stack?.split("\n")[3 + level] || "";
            const index = callerLine.indexOf("at ");
            const match = callerLine.match(/at ([\w\.]+)/);
            const callerName = match ? match[1] : "";
            return callerName;
        }
        catch (error) {
            return "";
        }
    }
    static assert(condition, message = null) {
        if (!condition) {
            throw new Error(message);
        }
    }
    static alert(text = '') {
        function getErrorObject() {
            return new Error('');
        }
        const err = getErrorObject();
        const caller_line = err.stack?.split("\n")[4];
        var index = caller_line?.indexOf("at ") ?? 0;
        var clean = caller_line?.slice(index + 2, caller_line.length);
        alert(text + "\n" + caller_line + "\n" + index + "\n" + clean);
    }
    static isOverlapping(x1, y1, w1, h1, x2, y2, w2, h2) {
        const left1 = x1;
        const right1 = x1 + w1;
        const top1 = y1;
        const bottom1 = y1 + h1;
        const left2 = x2;
        const right2 = x2 + w2;
        const top2 = y2;
        const bottom2 = y2 + h2;
        if (left1 >= right2 || left2 >= right1 || top1 >= bottom2 || top2 >= bottom1) {
            return null;
        }
        const overlapX = Math.max(left1, left2);
        const overlapY = Math.max(top1, top2);
        const overlapWidth = Math.min(right1, right2) - overlapX;
        const overlapHeight = Math.min(bottom1, bottom2) - overlapY;
        return {
            x: overlapX,
            y: overlapY,
            width: overlapWidth,
            height: overlapHeight
        };
    }
    static resetAndRemoveAnimation(element, class_name) {
        element.classList.remove(class_name);
        requestAnimationFrame(() => {
            element.classList.add(class_name);
            function handleAnimationEnd() {
                element.classList.remove(class_name);
                element.removeEventListener('animationend', handleAnimationEnd);
            }
            element.removeEventListener('animationend', handleAnimationEnd);
            element.addEventListener('animationend', handleAnimationEnd, { once: true });
        });
    }
}
Lib.cookie = Cookie;
Lib.array = MyArray;
Lib.object = MyObject;
Lib.loader = Loader;
Lib.client = Client;
Lib.string = MyString;
Lib.game = Game;
window.Lib = Lib;
//# sourceMappingURL=lib.js.map