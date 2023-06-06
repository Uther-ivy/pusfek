import execjs

js_infos="""const w2 = "zxcvbnmlkjhgfdsaqwertyuiop0987654321QWERTYUIOPLKJHGFDSAZXCVBNM"
    , Nue = w2 + "-@#$%^&*+!";
var IA = {};
var Jf = {};
var zhuanma;
!(function () {
    var Wf = {
        RFC1738: "RFC1738",
        RFC3986: "RFC3986"
    }
    var ym = {
        default: Wf.RFC3986,
        formatters: {
            RFC1738: function (e) {
                return Tq.call(e, Pq, "+")
            },
            RFC3986: function (e) {
                return String(e)
            }
        },
        RFC1738: Wf.RFC1738,
        RFC3986: Wf.RFC3986
    }
    Un = function () {
        for (var e = [], t = 0; t < 256; ++t)
            e.push("%" + ((t < 16 ? "0" : "") + t.toString(16)).toUpperCase());
        return e
    }()
    rA = function (t, n) {
        for (var r = n && n.plainObjects ? Object.create(null) : {}, o = 0; o < t.length; ++o)
            typeof t[o] < "u" && (r[o] = t[o]);
        return r
    }
    Lq = function (t, n) {
        return Object.keys(n).reduce(function (r, o) {
            return r[o] = n[o],
                r
        }, t)
    }
    Nq = function (e, t, n) {
        var r = e.replace(/\+/g, " ");
        if (n === "iso-8859-1")
            return r.replace(/%[0-9a-f]{2}/gi, unescape);
        try {
            return decodeURIComponent(r)
        } catch {
            return r
        }
    }
    Yq = function (t, n) {
        return [].concat(t, n)
    }
    Hq = function (t) {
        for (var n = [{
            obj: {
                o: t
            },
            prop: "o"
        }], r = [], o = 0; o < n.length; ++o)
            for (var u = n[o], i = u.obj[u.prop], s = Object.keys(i), a = 0; a < s.length; ++a) {
                var l = s[a]
                    , c = i[l];
                typeof c == "object" && c !== null && r.indexOf(c) === -1 && (n.push({
                    obj: i,
                    prop: l
                }),
                    r.push(c))
            }
        return Rq(n),
            t
    }
    jq = function (t, n, r, o, u) {
        if (t.length === 0)
            return t;
        var i = t;
        if (typeof t == "symbol" ? i = Symbol.prototype.toString.call(t) : typeof t != "string" && (i = String(t)),
        r === "iso-8859-1")
            return escape(i).replace(/%u[0-9a-f]{4}/gi, function (c) {
                return "%26%23" + parseInt(c.slice(2), 16) + "%3B"
            });
        for (var s = "", a = 0; a < i.length; ++a) {
            var l = i.charCodeAt(a);
            if (l === 45 || l === 46 || l === 95 || l === 126 || l >= 48 && l <= 57 || l >= 65 && l <= 90 || l >= 97 && l <= 122 || u === Iq.RFC1738 && (l === 40 || l === 41)) {
                s += i.charAt(a);
                continue
            }
            if (l < 128) {
                s = s + Un[l];
                continue
            }
            if (l < 2048) {
                s = s + (Un[192 | l >> 6] + Un[128 | l & 63]);
                continue
            }
            if (l < 55296 || l >= 57344) {
                s = s + (Un[224 | l >> 12] + Un[128 | l >> 6 & 63] + Un[128 | l & 63]);
                continue
            }
            a += 1,
                l = 65536 + ((l & 1023) << 10 | i.charCodeAt(a) & 1023),
                s += Un[240 | l >> 18] + Un[128 | l >> 12 & 63] + Un[128 | l >> 6 & 63] + Un[128 | l & 63]
        }
        return s
    }
    zq = function (t) {
        return !t || typeof t != "object" ? !1 : !!(t.constructor && t.constructor.isBuffer && t.constructor.isBuffer(t))
    }
    Vq = function (t) {
        return Object.prototype.toString.call(t) === "[object RegExp]"
    }
    Uq = function (t, n) {
        if (xu(t)) {
            for (var r = [], o = 0; o < t.length; o += 1)
                r.push(n(t[o]));
            return r
        }
        return n(t)
    }
    Mq = function e(t, n, r) {
        if (!n)
            return t;
        if (typeof n != "object") {
            if (xu(t))
                t.push(n);
            else if (t && typeof t == "object")
                (r && (r.plainObjects || r.allowPrototypes) || !Gf.call(Object.prototype, n)) && (t[n] = !0);
            else
                return [t, n];
            return t
        }
        if (!t || typeof t != "object")
            return [t].concat(n);
        var o = t;
        return xu(t) && !xu(n) && (o = rA(t, r)),
            xu(t) && xu(n) ? (n.forEach(function (u, i) {
                if (Gf.call(t, i)) {
                    var s = t[i];
                    s && typeof s == "object" && u && typeof u == "object" ? t[i] = e(s, u, r) : t.push(u)
                } else
                    t[i] = u
            }),
                t) : Object.keys(n).reduce(function (u, i) {
                var s = n[i];
                return Gf.call(u, i) ? u[i] = e(u[i], s, r) : u[i] = s,
                    u
            }, o)
    }
    var Iq = ym
    fm = Function.prototype.bind
    oa = fm
    $l = oa.call(Function.call, String.prototype.slice)
    I1 = oa.call(Function.call, String.prototype.replace)
    NG = /[^%.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|%$))/g
    HG = function (t) {
        var n = $l(t, 0, 1)
            , r = $l(t, -1);
        if (n === "%" && r !== "%")
            throw new ri("invalid intrinsic syntax, expected closing `%`");
        if (r === "%" && n !== "%")
            throw new ri("invalid intrinsic syntax, expected opening `%`");
        var o = [];
        return I1(t, NG, function (u, i, s, a) {
            o[o.length] = s ? I1(a, jG, "$1") : i || u
        }),
            o
    }
    P1 = {
        "%ArrayBufferPrototype%": ["ArrayBuffer", "prototype"],
        "%ArrayPrototype%": ["Array", "prototype"],
        "%ArrayProto_entries%": ["Array", "prototype", "entries"],
        "%ArrayProto_forEach%": ["Array", "prototype", "forEach"],
        "%ArrayProto_keys%": ["Array", "prototype", "keys"],
        "%ArrayProto_values%": ["Array", "prototype", "values"],
        "%AsyncFunctionPrototype%": ["AsyncFunction", "prototype"],
        "%AsyncGenerator%": ["AsyncGeneratorFunction", "prototype"],
        "%AsyncGeneratorPrototype%": ["AsyncGeneratorFunction", "prototype", "prototype"],
        "%BooleanPrototype%": ["Boolean", "prototype"],
        "%DataViewPrototype%": ["DataView", "prototype"],
        "%DatePrototype%": ["Date", "prototype"],
        "%ErrorPrototype%": ["Error", "prototype"],
        "%EvalErrorPrototype%": ["EvalError", "prototype"],
        "%Float32ArrayPrototype%": ["Float32Array", "prototype"],
        "%Float64ArrayPrototype%": ["Float64Array", "prototype"],
        "%FunctionPrototype%": ["Function", "prototype"],
        "%Generator%": ["GeneratorFunction", "prototype"],
        "%GeneratorPrototype%": ["GeneratorFunction", "prototype", "prototype"],
        "%Int8ArrayPrototype%": ["Int8Array", "prototype"],
        "%Int16ArrayPrototype%": ["Int16Array", "prototype"],
        "%Int32ArrayPrototype%": ["Int32Array", "prototype"],
        "%JSONParse%": ["JSON", "parse"],
        "%JSONStringify%": ["JSON", "stringify"],
        "%MapPrototype%": ["Map", "prototype"],
        "%NumberPrototype%": ["Number", "prototype"],
        "%ObjectPrototype%": ["Object", "prototype"],
        "%ObjProto_toString%": ["Object", "prototype", "toString"],
        "%ObjProto_valueOf%": ["Object", "prototype", "valueOf"],
        "%PromisePrototype%": ["Promise", "prototype"],
        "%PromiseProto_then%": ["Promise", "prototype", "then"],
        "%Promise_all%": ["Promise", "all"],
        "%Promise_reject%": ["Promise", "reject"],
        "%Promise_resolve%": ["Promise", "resolve"],
        "%RangeErrorPrototype%": ["RangeError", "prototype"],
        "%ReferenceErrorPrototype%": ["ReferenceError", "prototype"],
        "%RegExpPrototype%": ["RegExp", "prototype"],
        "%SetPrototype%": ["Set", "prototype"],
        "%SharedArrayBufferPrototype%": ["SharedArrayBuffer", "prototype"],
        "%StringPrototype%": ["String", "prototype"],
        "%SymbolPrototype%": ["Symbol", "prototype"],
        "%SyntaxErrorPrototype%": ["SyntaxError", "prototype"],
        "%TypedArrayPrototype%": ["TypedArray", "prototype"],
        "%TypeErrorPrototype%": ["TypeError", "prototype"],
        "%Uint8ArrayPrototype%": ["Uint8Array", "prototype"],
        "%Uint8ClampedArrayPrototype%": ["Uint8ClampedArray", "prototype"],
        "%Uint16ArrayPrototype%": ["Uint16Array", "prototype"],
        "%Uint32ArrayPrototype%": ["Uint32Array", "prototype"],
        "%URIErrorPrototype%": ["URIError", "prototype"],
        "%WeakMapPrototype%": ["WeakMap", "prototype"],
        "%WeakSetPrototype%": ["WeakSet", "prototype"]
    }
    BG = function () {
        return typeof T1 != "function" || typeof Symbol != "function" || typeof T1("foo") != "symbol" || typeof Symbol("bar") != "symbol" ? !1 : AG()
    }
    Gn = Object.getPrototypeOf || function (e) {
        return e.__proto__
    }
    Ao = BG()
    var Ne;
    var _o = {};
    var GF = Function;
    var ri = SyntaxError;
    No = TypeError
    TG = typeof Uint8Array > "u" ? Ne : Gn(Uint8Array)

    OG = function () {
        try {
            return arguments.callee,
                Hf
        } catch {
            try {
                return Vu(arguments, "callee").get
            } catch {
                return Hf
            }
        }
    }
    zu = {
        "%AggregateError%": typeof AggregateError > "u" ? Ne : AggregateError,
        "%Array%": Array,
        "%ArrayBuffer%": typeof ArrayBuffer > "u" ? Ne : ArrayBuffer,
        "%ArrayIteratorPrototype%": Ao ? Gn([][Symbol.iterator]()) : '',
        "%AsyncFromSyncIteratorPrototype%": '',
        "%AsyncFunction%": _o,
        "%AsyncGenerator%": _o,
        "%AsyncGeneratorFunction%": _o,
        "%AsyncIteratorPrototype%": _o,
        "%Atomics%": typeof Atomics > "u" ? '' : Atomics,
        "%BigInt%": typeof BigInt > "u" ? '' : BigInt,
        "%BigInt64Array%": typeof BigInt64Array > "u" ? '' : BigInt64Array,
        "%BigUint64Array%": typeof BigUint64Array > "u" ? '' : BigUint64Array,
        "%Boolean%": Boolean,
        "%DataView%": typeof DataView > "u" ? '' : DataView,
        "%Date%": Date,
        "%decodeURI%": decodeURI,
        "%decodeURIComponent%": decodeURIComponent,
        "%encodeURI%": encodeURI,
        "%encodeURIComponent%": encodeURIComponent,
        "%Error%": Error,
        "%eval%": eval,
        "%EvalError%": EvalError,
        "%Float32Array%": typeof Float32Array > "u" ? '' : Float32Array,
        "%Float64Array%": typeof Float64Array > "u" ? '' : Float64Array,
        "%FinalizationRegistry%": typeof FinalizationRegistry > "u" ? '' : FinalizationRegistry,
        "%Function%": GF,
        "%GeneratorFunction%": _o,
        "%Int8Array%": typeof Int8Array > "u" ? '' : Int8Array,
        "%Int16Array%": typeof Int16Array > "u" ? '' : Int16Array,
        "%Int32Array%": typeof Int32Array > "u" ? '' : Int32Array,
        "%isFinite%": isFinite,
        "%isNaN%": isNaN,
        "%IteratorPrototype%": Ao ? Gn(Gn([][Symbol.iterator]())) : '',
        "%JSON%": typeof JSON == "object" ? JSON : '',
        "%Map%": typeof Map > "u" ? '' : Map,
        "%MapIteratorPrototype%": typeof Map > "u" || !Ao ? '' : Gn(new Map()[Symbol.iterator]()),
        "%Math%": Math,
        "%Number%": Number,
        "%Object%": Object,
        "%parseFloat%": parseFloat,
        "%parseInt%": parseInt,
        "%Promise%": typeof Promise > "u" ? '' : Promise,
        "%Proxy%": typeof Proxy > "u" ? '' : Proxy,
        "%RangeError%": RangeError,
        "%ReferenceError%": ReferenceError,
        "%Reflect%": typeof Reflect > "u" ? Ne : Reflect,
        "%RegExp%": RegExp,
        "%Set%": typeof Set > "u" ? Ne : Set,
        "%SetIteratorPrototype%": typeof Set > "u" || !Ao ? Ne : Gn(new Set()[Symbol.iterator]()),
        "%SharedArrayBuffer%": typeof SharedArrayBuffer > "u" ? Ne : SharedArrayBuffer,
        "%String%": String,
        "%StringIteratorPrototype%": Ao ? Gn(""[Symbol.iterator]()) : Ne,
        "%Symbol%": Ao ? Symbol : Ne,
        "%SyntaxError%": ri,
        "%ThrowTypeError%": OG,
        "%TypedArray%": TG,
        "%TypeError%": No,
        "%Uint8Array%": typeof Uint8Array > "u" ? Ne : Uint8Array,
        "%Uint8ClampedArray%": typeof Uint8ClampedArray > "u" ? Ne : Uint8ClampedArray,
        "%Uint16Array%": typeof Uint16Array > "u" ? Ne : Uint16Array,
        "%Uint32Array%": typeof Uint32Array > "u" ? Ne : Uint32Array,
        "%URIError%": URIError,
        "%WeakMap%": typeof WeakMap > "u" ? Ne : WeakMap,
        "%WeakRef%": typeof WeakRef > "u" ? Ne : WeakRef,
        "%WeakSet%": typeof WeakSet > "u" ? Ne : WeakSet
    }
    xG = fm
    kG = xG.call(Function.call, Object.prototype.hasOwnProperty)
    Zl = kG
    LG = oa.call(Function.call, RegExp.prototype.exec)
    VG = function (t, n) {
        var r = t, o;
        if (Zl(P1, r) && (o = P1[r],
            r = "%" + o[0] + "%"),
            Zl(zu, r)) {
            var u = zu[r];
            if (u === _o && (u = IG(r)),
            typeof u > "u" && !n)
                throw new No("intrinsic " + t + " exists, but is not available. Please file an issue!");
            return {
                alias: o,
                name: r,
                value: u
            }
        }
        throw new ri("intrinsic " + t + " does not exist!")
    }
    hm = function (t, n) {
        if (typeof t != "string" || t.length === 0)
            throw new No("intrinsic name must be a non-empty string");
        if (arguments.length > 1 && typeof n != "boolean")
            throw new No('"allowMissing" argument must be a boolean');
        if (LG(/^%?[^%]*%?$/, t) === null)
            throw new ri("`%` may not be present anywhere but at the beginning and end of the intrinsic name");
        var r = HG(t)
            , o = r.length > 0 ? r[0] : ""
            , u = VG("%" + o + "%", n)
            , i = u.name
            , s = u.value
            , a = !1
            , l = u.alias;
        l && (o = l[0],
            MG(r, RG([0, 1], l)));
        for (var c = 1, d = !0; c < r.length; c += 1) {
            var f = r[c]
                , p = $l(f, 0, 1)
                , h = $l(f, -1);
            if ((p === '"' || p === "'" || p === "`" || h === '"' || h === "'" || h === "`") && p !== h)
                throw new ri("property names with quotes must have matching quotes");
            if ((f === "constructor" || !d) && (a = !0),
                o += "." + f,
                i = "%" + o + "%",
                Zl(zu, i))
                s = zu[i];
            else if (s != null) {
                if (!(f in s)) {
                    if (!n)
                        throw new No("base intrinsic for " + t + " exists, but the property is not available.");
                    return
                }
                if (Vu && c + 1 >= r.length) {
                    var g = Vu(s, f);
                    d = !!g,
                        d && "get" in g && !("originalValue" in g.get) ? s = g.get : s = s[f]
                } else
                    d = Zl(s, f),
                        s = s[f];
                d && !a && (zu[i] = s)
            }
        }
        return s
    }
    uA = {
        arrayToObject: rA,
        assign: Lq,
        combine: Yq,
        compact: Hq,
        decode: Nq,
        encode: jq,
        isBuffer: zq,
        isRegExp: Vq,
        maybeMap: Uq,
        merge: Mq
    }


    Gq = Array.prototype.push
    var qf = {};
    vm = hm
    Kq = function (t) {
        return typeof t == "string" || typeof t == "number" || typeof t == "boolean" || typeof t == "symbol" || typeof t == "bigint"
    }
    Qq = function e(t, n, r, o, u, i, s, a, l, c, d, f, p, h, g, C) {
        for (var m = t, E = C, y = 0, v = !1; (E = E.get(qf)) !== void 0 && !v;) {
            var F = E.get(t);
            if (y += 1,
            typeof F < "u") {
                if (F === y)
                    throw new RangeError("Cyclic object value");
                v = !0
            }
            typeof E.get(qf) > "u" && (y = 0)
        }
        if (typeof a == "function" ? m = a(n, m) : m instanceof Date ? m = d(m) : r === "comma" && mr(m) && (m = pl.maybeMap(m, function (N) {
            return N instanceof Date ? d(N) : N
        })),
        m === null) {
            if (u)
                return s && !h ? s(n, xt.encoder, g, "key", f) : n;
            m = ""
        }
        if (Kq(m) || pl.isBuffer(m)) {
            if (s) {
                var B = h ? n : s(n, xt.encoder, g, "key", f);
                return [p(B) + "=" + p(s(m, xt.encoder, g, "value", f))]
            }
            return [p(n) + "=" + p(String(m))]
        }
        var S = [];
        if (typeof m > "u")
            return S;
        var T;
        if (r === "comma" && mr(m))
            h && s && (m = pl.maybeMap(m, s)),
                T = [{
                    value: m.length > 0 ? m.join(",") || null : void 0
                }];
        else if (mr(a))
            T = a;
        else {
            var O = Object.keys(m);
            T = l ? O.sort(l) : O
        }
        for (var P = o && mr(m) && m.length === 1 ? n + "[]" : n, W = 0; W < T.length; ++W) {
            var M = T[W]
                , H = typeof M == "object" && typeof M.value < "u" ? M.value : m[M];
            if (!(i && H === null)) {
                var z = mr(m) ? typeof r == "function" ? r(P, M) : P : P + (c ? "." + M : "[" + M + "]");
                C.set(t, y);
                var G = oA();
                G.set(qf, C),
                    iA(S, e(H, z, r, o, u, i, r === "comma" && h && mr(m) ? null : s, a, l, c, d, f, p, h, g, G))
            }
        }
        return S
    }
    iA = function (e, t) {
        Gq.apply(e, mr(t) ? t : [t])
    }
    Va = vm("%WeakMap%", !0)
    Oq = function () {
        var t, n, r, o = {
            assert: function (u) {
                if (!o.has(u))
                    throw new Fq("Side channel does not contain " + Cq(u))
            },
            get: function (u) {
                if (Va && u && (typeof u == "object" || typeof u == "function")) {
                    if (t)
                        return Aq(t, u)
                } else if (za) {
                    if (n)
                        return wq(n, u)
                } else if (r)
                    return _q(r, u)
            },
            has: function (u) {
                if (Va && u && (typeof u == "object" || typeof u == "function")) {
                    if (t)
                        return bq(t, u)
                } else if (za) {
                    if (n)
                        return Sq(n, u)
                } else if (r)
                    return kq(r, u);
                return !1
            },
            set: function (u, i) {
                Va && u && (typeof u == "object" || typeof u == "function") ? (t || (t = new Va),
                    Bq(t, u, i)) : za ? (n || (n = new za),
                    Dq(n, u, i)) : (r || (r = {
                    key: {},
                    next: null
                }),
                    xq(r, u, i))
            }
        };
        return o
    }
    q1 = {
        brackets: function (t) {
            return t + "[]"
        },
        comma: "comma",
        indices: function (t, n) {
            return t + "[" + n + "]"
        },
        repeat: function (t) {
            return t
        }
    }
    var cs = ym
    var pl = uA
    var K1 = cs.default
    var mr = Array.isArray
    var oA = Oq
    xt = {
        addQueryPrefix: !1,
        allowDots: !1,
        charset: "utf-8",
        charsetSentinel: !1,
        delimiter: "&",
        encode: !0,
        encoder: pl.encode,
        encodeValuesOnly: !1,
        format: K1,
        formatter: cs.formatters[K1],
        indices: !1,
        serializeDate: function (t) {
            return qq.call(t)
        },
        skipNulls: !1,
        strictNullHandling: !1
    }
    ym = {
        default: Wf.RFC3986,
        formatters: {
            RFC1738: function (e) {
                return Tq.call(e, Pq, "+")
            },
            RFC3986: function (e) {
                return String(e)
            }
        },
        RFC1738: Wf.RFC1738,
        RFC3986: Wf.RFC3986
    }


    Jq = function (t) {
        cs = ym
        if (!t)
            return xt;
        if (t.encoder !== null && typeof t.encoder < "u" && typeof t.encoder != "function")
            throw new TypeError("Encoder has to be a function.");
        var n = t.charset || xt.charset;
        if (typeof t.charset < "u" && t.charset !== "utf-8" && t.charset !== "iso-8859-1")
            throw new TypeError("The charset option must be either utf-8, iso-8859-1, or undefined");
        var r = cs.default;
        if (typeof t.format < "u") {
            if (!Wq.call(cs.formatters, t.format))
                throw new TypeError("Unknown format option provided.");
            r = t.format
        }
        var o = cs.formatters[r]
            , u = xt.filter;
        return (typeof t.filter == "function" || mr(t.filter)) && (u = t.filter),
            {
                addQueryPrefix: typeof t.addQueryPrefix == "boolean" ? t.addQueryPrefix : xt.addQueryPrefix,
                allowDots: typeof t.allowDots > "u" ? xt.allowDots : !!t.allowDots,
                charset: n,
                charsetSentinel: typeof t.charsetSentinel == "boolean" ? t.charsetSentinel : xt.charsetSentinel,
                delimiter: typeof t.delimiter > "u" ? xt.delimiter : t.delimiter,
                encode: typeof t.encode == "boolean" ? t.encode : xt.encode,
                encoder: typeof t.encoder == "function" ? t.encoder : xt.encoder,
                encodeValuesOnly: typeof t.encodeValuesOnly == "boolean" ? t.encodeValuesOnly : xt.encodeValuesOnly,
                filter: u,
                format: r,
                formatter: o,
                serializeDate: typeof t.serializeDate == "function" ? t.serializeDate : xt.serializeDate,
                skipNulls: typeof t.skipNulls == "boolean" ? t.skipNulls : xt.skipNulls,
                sort: typeof t.sort == "function" ? t.sort : null,
                strictNullHandling: typeof t.strictNullHandling == "boolean" ? t.strictNullHandling : xt.strictNullHandling
            }
    }
    zhuanma = function (e, t) {
        var n = e, r = Jq(t), o, u;
        typeof r.filter == "function" ? (u = r.filter,
            n = u("", n)) : mr(r.filter) && (u = r.filter,
            o = u);
        var i = [];
        if (typeof n != "object" || n === null)
            return "";
        var s;
        t && t.arrayFormat in q1 ? s = t.arrayFormat : t && "indices" in t ? s = t.indices ? "indices" : "repeat" : s = "indices";
        var a = q1[s];
        if (t && "commaRoundTrip" in t && typeof t.commaRoundTrip != "boolean")
            throw new TypeError("`commaRoundTrip` must be a boolean, or absent");
        var l = a === "comma" && t && t.commaRoundTrip;
        o || (o = Object.keys(n)),
        r.sort && o.sort(r.sort);
        for (var c = oA(), d = 0; d < o.length; ++d) {
            var f = o[d];
            r.skipNulls && n[f] === null || iA(i, Qq(n[f], f, a, l, r.strictNullHandling, r.skipNulls, r.encode ? r.encoder : null, r.filter, r.sort, r.allowDots, r.serializeDate, r.format, r.formatter, r.encodeValuesOnly, r.charset, c))
        }
        var p = i.join(r.delimiter)
            , h = r.addQueryPrefix === !0 ? "?" : "";
        return r.charsetSentinel && (r.charset === "iso-8859-1" ? h += "utf8=%26%2310003%3B&" : h += "utf8=%E2%9C%93&"),
            p.length > 0 ? h + p : ""
    }
})()

function xJ() {

    return function (e, t) {
        (function (n, r) {
                e.exports = r()
            }
        )(this, function () {
            var n = n || function (r, o) {
                var u;
                if (typeof window < "u" && window.crypto && (u = window.crypto),
                typeof self < "u" && self.crypto && (u = self.crypto),
                typeof globalThis < "u" && globalThis.crypto && (u = globalThis.crypto),
                !u && typeof window < "u" && window.msCrypto && (u = window.msCrypto),
                !u && typeof Pu < "u" && Pu.crypto && (u = Pu.crypto),
                !u && typeof _J == "function")
                    try {
                        u = JF
                    } catch {
                    }
                var i = function () {
                    if (u) {
                        if (typeof u.getRandomValues == "function")
                            try {
                                return u.getRandomValues(new Uint32Array(1))[0]
                            } catch {
                            }
                        if (typeof u.randomBytes == "function")
                            try {
                                return u.randomBytes(4).readInt32LE()
                            } catch {
                            }
                    }
                    throw new Error("Native crypto module could not be used to get secure random number.")
                }
                    , s = Object.create || function () {
                    function E() {
                    }

                    return function (y) {
                        var v;
                        return E.prototype = y,
                            v = new E,
                            E.prototype = null,
                            v
                    }
                }()
                    , a = {}
                    , l = a.lib = {}
                    , c = l.Base = function () {
                    return {
                        extend: function (E) {
                            var y = s(this);
                            return E && y.mixIn(E),
                            (!y.hasOwnProperty("init") || this.init === y.init) && (y.init = function () {
                                    y.$super.init.apply(this, arguments)
                                }
                            ),
                                y.init.prototype = y,
                                y.$super = this,
                                y
                        },
                        create: function () {
                            var E = this.extend();
                            return E.init.apply(E, arguments),
                                E
                        },
                        init: function () {
                        },
                        mixIn: function (E) {
                            for (var y in E)
                                E.hasOwnProperty(y) && (this[y] = E[y]);
                            E.hasOwnProperty("toString") && (this.toString = E.toString)
                        },
                        clone: function () {
                            return this.init.prototype.extend(this)
                        }
                    }
                }()
                    , d = l.WordArray = c.extend({
                    init: function (E, y) {
                        E = this.words = E || [],
                            y != o ? this.sigBytes = y : this.sigBytes = E.length * 4
                    },
                    toString: function (E) {
                        return (E || p).stringify(this)
                    },
                    concat: function (E) {
                        var y = this.words
                            , v = E.words
                            , F = this.sigBytes
                            , B = E.sigBytes;
                        if (this.clamp(),
                        F % 4)
                            for (var S = 0; S < B; S++) {
                                var T = v[S >>> 2] >>> 24 - S % 4 * 8 & 255;
                                y[F + S >>> 2] |= T << 24 - (F + S) % 4 * 8
                            }
                        else
                            for (var O = 0; O < B; O += 4)
                                y[F + O >>> 2] = v[O >>> 2];
                        return this.sigBytes += B,
                            this
                    },
                    clamp: function () {
                        var E = this.words
                            , y = this.sigBytes;
                        E[y >>> 2] &= 4294967295 << 32 - y % 4 * 8,
                            E.length = r.ceil(y / 4)
                    },
                    clone: function () {
                        var E = c.clone.call(this);
                        return E.words = this.words.slice(0),
                            E
                    },
                    random: function (E) {
                        for (var y = [], v = 0; v < E; v += 4)
                            y.push(i());
                        return new d.init(y, E)
                    }
                })
                    , f = a.enc = {}
                    , p = f.Hex = {
                    stringify: function (E) {
                        for (var y = E.words, v = E.sigBytes, F = [], B = 0; B < v; B++) {
                            var S = y[B >>> 2] >>> 24 - B % 4 * 8 & 255;
                            F.push((S >>> 4).toString(16)),
                                F.push((S & 15).toString(16))
                        }
                        return F.join("")
                    },
                    parse: function (E) {
                        for (var y = E.length, v = [], F = 0; F < y; F += 2)
                            v[F >>> 3] |= parseInt(E.substr(F, 2), 16) << 24 - F % 8 * 4;
                        return new d.init(v, y / 2)
                    }
                }
                    , h = f.Latin1 = {
                    stringify: function (E) {
                        for (var y = E.words, v = E.sigBytes, F = [], B = 0; B < v; B++) {
                            var S = y[B >>> 2] >>> 24 - B % 4 * 8 & 255;
                            F.push(String.fromCharCode(S))
                        }
                        return F.join("")
                    },
                    parse: function (E) {
                        for (var y = E.length, v = [], F = 0; F < y; F++)
                            v[F >>> 2] |= (E.charCodeAt(F) & 255) << 24 - F % 4 * 8;
                        return new d.init(v, y)
                    }
                }
                    , g = f.Utf8 = {
                    stringify: function (E) {
                        try {
                            return decodeURIComponent(escape(h.stringify(E)))
                        } catch {
                            throw new Error("Malformed UTF-8 data")
                        }
                    },
                    parse: function (E) {
                        return h.parse(unescape(encodeURIComponent(E)))
                    }
                }
                    , C = l.BufferedBlockAlgorithm = c.extend({
                    reset: function () {
                        this._data = new d.init,
                            this._nDataBytes = 0
                    },
                    _append: function (E) {
                        typeof E == "string" && (E = g.parse(E)),
                            this._data.concat(E),
                            this._nDataBytes += E.sigBytes
                    },
                    _process: function (E) {
                        var y, v = this._data, F = v.words, B = v.sigBytes, S = this.blockSize, T = S * 4, O = B / T;
                        E ? O = r.ceil(O) : O = r.max((O | 0) - this._minBufferSize, 0);
                        var P = O * S
                            , W = r.min(P * 4, B);
                        if (P) {
                            for (var M = 0; M < P; M += S)
                                this._doProcessBlock(F, M);
                            y = F.splice(0, P),
                                v.sigBytes -= W
                        }
                        return new d.init(y, W)
                    },
                    clone: function () {
                        var E = c.clone.call(this);
                        return E._data = this._data.clone(),
                            E
                    },
                    _minBufferSize: 0
                });
                l.Hasher = C.extend({
                    cfg: c.extend(),
                    init: function (E) {
                        this.cfg = this.cfg.extend(E),
                            this.reset()
                    },
                    reset: function () {
                        C.reset.call(this),
                            this._doReset()
                    },
                    update: function (E) {
                        return this._append(E),
                            this._process(),
                            this
                    },
                    finalize: function (E) {
                        E && this._append(E);
                        var y = this._doFinalize();
                        return y
                    },
                    blockSize: 16,
                    _createHelper: function (E) {
                        return function (y, v) {
                            return new E.init(v).finalize(y)
                        }
                    },
                    _createHmacHelper: function (E) {
                        return function (y, v) {
                            return new m.HMAC.init(E, v).finalize(y)
                        }
                    }
                });
                var m = a.algo = {};
                return a
            }(Math);
            return n
        })
    }(Jf),
        Jf.exports
}

!(function (e, t) {
        (function (n, r) {
                e.exports = r(xJ())
            }
        )(this, function (n) {
            return function (r) {
                var o = n
                    , u = o.lib
                    , i = u.WordArray
                    , s = u.Hasher
                    , a = o.algo
                    , l = []
                    , c = [];
                (function () {
                        function p(m) {
                            for (var E = r.sqrt(m), y = 2; y <= E; y++)
                                if (!(m % y))
                                    return !1;
                            return !0
                        }

                        function h(m) {
                            return (m - (m | 0)) * 4294967296 | 0
                        }

                        for (var g = 2, C = 0; C < 64;)
                            p(g) && (C < 8 && (l[C] = h(r.pow(g, 1 / 2))),
                                c[C] = h(r.pow(g, 1 / 3)),
                                C++),
                                g++
                    }
                )();
                var d = []
                    , f = a.SHA256 = s.extend({
                    _doReset: function () {
                        this._hash = new i.init(l.slice(0))
                    },
                    _doProcessBlock: function (p, h) {
                        for (var g = this._hash.words, C = g[0], m = g[1], E = g[2], y = g[3], v = g[4], F = g[5], B = g[6], S = g[7], T = 0; T < 64; T++) {
                            if (T < 16)
                                d[T] = p[h + T] | 0;
                            else {
                                var O = d[T - 15]
                                    , P = (O << 25 | O >>> 7) ^ (O << 14 | O >>> 18) ^ O >>> 3
                                    , W = d[T - 2]
                                    , M = (W << 15 | W >>> 17) ^ (W << 13 | W >>> 19) ^ W >>> 10;
                                d[T] = P + d[T - 7] + M + d[T - 16]
                            }
                            var H = v & F ^ ~v & B
                                , z = C & m ^ C & E ^ m & E
                                , G = (C << 30 | C >>> 2) ^ (C << 19 | C >>> 13) ^ (C << 10 | C >>> 22)
                                , N = (v << 26 | v >>> 6) ^ (v << 21 | v >>> 11) ^ (v << 7 | v >>> 25)
                                , I = S + N + H + c[T] + d[T]
                                , Z = G + z;
                            S = B,
                                B = F,
                                F = v,
                                v = y + I | 0,
                                y = E,
                                E = m,
                                m = C,
                                C = I + Z | 0
                        }
                        g[0] = g[0] + C | 0,
                            g[1] = g[1] + m | 0,
                            g[2] = g[2] + E | 0,
                            g[3] = g[3] + y | 0,
                            g[4] = g[4] + v | 0,
                            g[5] = g[5] + F | 0,
                            g[6] = g[6] + B | 0,
                            g[7] = g[7] + S | 0
                    },
                    _doFinalize: function () {
                        var p = this._data
                            , h = p.words
                            , g = this._nDataBytes * 8
                            , C = p.sigBytes * 8;
                        return h[C >>> 5] |= 128 << 24 - C % 32,
                            h[(C + 64 >>> 9 << 4) + 14] = r.floor(g / 4294967296),
                            h[(C + 64 >>> 9 << 4) + 15] = g,
                            p.sigBytes = h.length * 4,
                            this._process(),
                            this._hash
                    },
                    clone: function () {
                        var p = s.clone.call(this);
                        return p._hash = this._hash.clone(),
                            p
                    }
                });
                o.SHA256 = s._createHelper(f),
                    o.HmacSHA256 = s._createHmacHelper(f)
            }(Math),
                n.SHA256
        })
    }
)(IA);
const kJ = IA.exports;

function Au(e = []) {
    return e.map(t => Nue[t]).join("")
}

function jue(e) {
    return [...Array(e)].map(() => w2[Lue(0, 61)]).join("")
}

function Au(e = []) {
    return e.map(t => Nue[t]).join("")
}

function Lue(e, t) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * e + 1, 10);
        case 2:
            return parseInt(Math.random() * (t - e + 1) + e, 10);
        default:
            return 0
    }
}

function Hue(e) {
    let t = "";
    return typeof e == "object" ? t = Object.keys(e).map(n => `${n}=${e[n]}`).sort().join("&") : typeof e == "string" && (t = e.split("&").sort().join("&")),
        t
}

function Pv(e = {}) {
    const {p: t, t: n, n: r, k: o} = e
        , u = Hue(t);
    return kJ(r + o + decodeURIComponent(u) + n)

}

function r(ww) {
    o= w[0]
    data1=w[1]
    const a = Date.now()
        , l = jue(16)
        , c = Au([8, 28, 20, 42, 21, 53, 65, 6])
        , d = {
        [Au([56, 62, 52, 11, 23, 62, 39, 18, 16, 62, 54, 25, 25])]: Au([11, 11, 0, 21, 62, 25, 24, 19, 20, 15, 7]),
        [Au([56, 62, 52, 11, 23, 62, 39, 18, 16, 62, 60, 24, 5, 2, 18])]: l,
        [Au([56, 62, 52, 11, 23, 62, 39, 18, 16, 62, 40, 23, 6, 18, 14, 20, 15, 6, 25])]: a
    };
    if (o.toLowerCase() === "get") {
        (i == null ? void 0 : i.siteCode) === void 0 && !s.includes("?siteCode=") && (i ? o.params.siteCode = u.currentSite : o.params = {
            siteCode: u.currentSite
        });
        const f = Pv({
            p: i,
            t: a,
            n: l,
            k: c
        });
        d[[Au([56, 62, 52, 11, 23, 62, 39, 18, 16, 62, 53, 23, 11, 5, 15, 20, 22, 19, 18])]] = f
    } else {
        const f = Pv({
            p: zhuanma(data1, {allowDots: !0}),
            t: a,
            n: l,
            k: c
        });

        d[[Au([56, 62, 52, 11, 23, 62, 39, 18, 16, 62, 53, 23, 11, 5, 15, 20, 22, 19, 18])]] = f.toString()
        // console.log(String.fromCharCode.apply(null, new Uint8Array(d['X-Dgi-Req-Signature'][words])))
    }
    return o.headers = {
        ...d,
        ...o.headers
    }
}

console.log(r('post', {
    "keyword": "中标",
    "type": "trading-type",
    "secondType": "",
    "siteCode": "441900",
    "publishStartTime": "20230307000000",
    "publishEndTime": "20230407235959",
    "total": "94",
    "pageNo": 8,
    "pageSize": 10,
    "openConvert": false
}))"""


false=''
dsd={
    "keyword": "中标",
    "type": "trading-type",
    "secondType": "",
    "siteCode": "441900",
    "publishStartTime": "20230307000000",
    "publishEndTime": "20230407235959",
    "total": "94",
    "pageNo": 8,
    "pageSize": 10,
    "openConvert": false
}
sss=['post',dsd]

dedata = execjs.compile(js_infos).call('ss', sss)
print(dedata)