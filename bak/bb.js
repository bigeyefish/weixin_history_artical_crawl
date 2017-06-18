define("biz_common/dom/event.js", [], function () {
    "use strict";
    function e(e, t, n, o) {
        r.isPc || r.isWp ? i(e, "click", o, t, n) : i(e, "touchend", o, function (e) {
            if (-1 == r.tsTime || +new Date - r.tsTime > 200)return r.tsTime = -1, !1;
            var n = e.changedTouches[0];
            return Math.abs(r.y - n.clientY) <= 5 && Math.abs(r.x - n.clientX) <= 5 ? t.call(this, e) : void 0;
        }, n);
    }

    function t(e, t) {
        if (!e || !t || e.nodeType != e.ELEMENT_NODE)return !1;
        var n = e.webkitMatchesSelector || e.msMatchesSelector || e.matchesSelector;
        return n ? n.call(e, t) : (t = t.substr(1), e.className.indexOf(t) > -1);
    }

    function n(e, n, i) {
        for (; e && !t(e, n);)e = e !== i && e.nodeType !== e.DOCUMENT_NODE && e.parentNode;
        return e;
    }

    function i(t, i, o, a, c) {
        var s, d, u;
        return "input" == i && r.isPc, t ? ("function" == typeof o && (c = a, a = o, o = ""), "string" != typeof o && (o = ""),
            t == window && "load" == i && /complete|loaded/.test(document.readyState) ? a({
                type: "load"
            }) : "tap" == i ? e(t, a, c, o) : ("unload" == i && "onpagehide" in window && (i = "pagehide"), s = function (e) {
                var t = a(e);
                return t === !1 && (e.stopPropagation && e.stopPropagation(), e.preventDefault && e.preventDefault()),
                    t;
            }, o && "." == o.charAt(0) && (u = function (e) {
                var i = e.target || e.srcElement, a = n(i, o, t);
                return a ? (e.delegatedTarget = a, s(e)) : void 0;
            }), d = u || s, a[i + "_handler"] = d, t.addEventListener ? void t.addEventListener(i, d, !!c) : t.attachEvent ? void t.attachEvent("on" + i, d, !!c) : void 0)) : void 0;
    }

    function o(e, t, n, i) {
        if (e) {
            var o = n[t + "_handler"] || n;
            return e.removeEventListener ? void e.removeEventListener(t, o, !!i) : e.detachEvent ? void e.detachEvent("on" + t, o, !!i) : void 0;
        }
    }

    var a = navigator.userAgent, r = {
        isPc: /(WindowsNT)|(Windows NT)|(Macintosh)/i.test(navigator.userAgent),
        isWp: /Windows\sPhone/i.test(a),
        tsTime: -1
    };
    return r.isPc || i(document, "touchstart", function (e) {
        var t = e.changedTouches[0];
        r.x = t.clientX, r.y = t.clientY, r.tsTime = +new Date;
    }), {
        on: i,
        off: o,
        tap: e
    };
})//# sourceURL=biz_common/dom/event.js
//@ sourceURL=biz_common/dom/event.js