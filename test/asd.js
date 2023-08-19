
var v, b = {
            decode: function(e) {
                var t;
                if (void 0 === d) {
                    var n = "0123456789ABCDEF"
                      , r = " \f\n\r\t \u2028\u2029";
                    for (d = {},
                    t = 0; t < 16; ++t)
                        d[n.charAt(t)] = t;
                    for (n = n.toLowerCase(),
                    t = 10; t < 16; ++t)
                        d[n.charAt(t)] = t;
                    for (t = 0; t < r.length; ++t)
                        d[r.charAt(t)] = -1
                }
                var o = []
                  , i = 0
                  , s = 0;
                for (t = 0; t < e.length; ++t) {
                    var a = e.charAt(t);
                    if ("=" == a)
                        break;
                    if (a = d[a],
                    -1 != a) {
                        if (void 0 === a)
                            throw new Error("Illegal character at offset " + t);
                        i |= a,
                        ++s >= 2 ? (o[o.length] = i,
                        i = 0,
                        s = 0) : i <<= 4
                    }
                }
                if (s)
                    throw new Error("Hex encoding incomplete: 4 bits missing");
                return o
            }
        },
    g={decode:function(e) {
            var t;
            if (void 0 === v) {
                var n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
                    , r = "= \f\n\r\t \u2028\u2029";
                for (v = Object.create(null),
                         t = 0; t < 64; ++t)
                    v[n.charAt(t)] = t;
                for (v["-"] = 62,
                         v["_"] = 63,
                         t = 0; t < r.length; ++t)
                    v[r.charAt(t)] = -1
            }
            var o = []
                , i = 0
                , s = 0;
            for (t = 0; t < e.length; ++t) {
                var a = e.charAt(t);
                if ("=" == a)
                    break;
                if (a = v[a],
                -1 != a) {
                    if (void 0 === a)
                        throw new Error("Illegal character at offset " + t);
                    i |= a,
                        ++s >= 4 ? (o[o.length] = i >> 16,
                            o[o.length] = i >> 8 & 255,
                            o[o.length] = 255 & i,
                            i = 0,
                            s = 0) : i <<= 6
                }
            }
            switch (s) {
                case 1:
                    throw new Error("Base64 encoding incomplete: at least 2 bits missing");
                case 2:
                    o[o.length] = i >> 10;
                    break;
                case 3:
                    o[o.length] = i >> 16,
                        o[o.length] = i >> 8 & 255;
                    break
            }
            return o
        },
    re: /-----BEGIN [^-]+-----([A-Za-z0-9+\/=\s]+)-----END [^-]+-----|begin-base64[^\n]+\n([A-Za-z0-9+\/=\s]+)====/,
    unarmor: function(e) {
                    var t = g.re.exec(e);
                    if (t)
                        if (t[1])
                            e = t[1];
                        else {
                            if (!t[2])
                                throw new Error("RegExp out of sync");
                            e = t[2]
                        }
                    return g.decode(e)
                }
            },
    y = 1e13,
    _ = function() {
                function e(e) {
                    this.buf = [+e || 0]
                }
                return e.prototype.mulAdd = function(e, t) {
                    var n, r, o = this.buf, i = o.length;
                    for (n = 0; n < i; ++n)
                        r = o[n] * e + t,
                        r < y ? t = 0 : (t = 0 | r / y,
                        r -= t * y),
                        o[n] = r;
                    t > 0 && (o[n] = t)
                }
                ,
                e.prototype.sub = function(e) {
                    var t, n, r = this.buf, o = r.length;
                    for (t = 0; t < o; ++t)
                        n = r[t] - e,
                        n < 0 ? (n += y,
                        e = 1) : e = 0,
                        r[t] = n;
                    while (0 === r[r.length - 1])
                        r.pop()
                }
                ,
                e.prototype.toString = function(e) {
                    if (10 != (e || 10))
                        throw new Error("only base 10 is supported");
                    for (var t = this.buf, n = t[t.length - 1].toString(), r = t.length - 2; r >= 0; --r)
                        n += (y + t[r]).toString().substring(1);
                    return n
                }
                ,
                e.prototype.valueOf = function() {
                    for (var e = this.buf, t = 0, n = e.length - 1; n >= 0; --n)
                        t = t * y + e[n];
                    return t
                }
                ,
                e.prototype.simplify = function() {
                    var e = this.buf;
                    return 1 == e.length ? e[0] : this
                }
                ,
                e
            }(),
    x = "…",
    w = /^(\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([01]\d|2[0-3])(?:([0-5]\d)(?:([0-5]\d)(?:[.,](\d{1,3}))?)?)?(Z|[-+](?:[0]\d|1[0-2])([0-5]\d)?)?$/,
    C = /^(\d\d\d\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([01]\d|2[0-3])(?:([0-5]\d)(?:([0-5]\d)(?:[.,](\d{1,3}))?)?)?(Z|[-+](?:[0]\d|1[0-2])([0-5]\d)?)?$/;
    function j(e, t) {
                return e.length > t && (e = e.substring(0, t) + x),
                e
            }

var S, M = function() {
            function e(t, n) {
                this.hexDigits = "0123456789ABCDEF",
                t instanceof e ? (this.enc = t.enc,
                this.pos = t.pos) : (this.enc = t,
                this.pos = n)
            }
            return e.prototype.get = function(e) {
                if (void 0 === e && (e = this.pos++),
                e >= this.enc.length)
                    throw new Error("Requesting byte offset " + e + " on a stream of length " + this.enc.length);
                return "string" === typeof this.enc ? this.enc.charCodeAt(e) : this.enc[e]
            }
            ,
            e.prototype.hexByte = function(e) {
                return this.hexDigits.charAt(e >> 4 & 15) + this.hexDigits.charAt(15 & e)
            }
            ,
            e.prototype.hexDump = function(e, t, n) {
                for (var r = "", o = e; o < t; ++o)
                    if (r += this.hexByte(this.get(o)),
                    !0 !== n)
                        switch (15 & o) {
                        case 7:
                            r += "  ";
                            break;
                        case 15:
                            r += "\n";
                            break;
                        default:
                            r += " "
                        }
                return r
            }
            ,
            e.prototype.isASCII = function(e, t) {
                for (var n = e; n < t; ++n) {
                    var r = this.get(n);
                    if (r < 32 || r > 176)
                        return !1
                }
                return !0
            }
            ,
            e.prototype.parseStringISO = function(e, t) {
                for (var n = "", r = e; r < t; ++r)
                    n += String.fromCharCode(this.get(r));
                return n
            }
            ,
            e.prototype.parseStringUTF = function(e, t) {
                for (var n = "", r = e; r < t; ) {
                    var o = this.get(r++);
                    n += o < 128 ? String.fromCharCode(o) : o > 191 && o < 224 ? String.fromCharCode((31 & o) << 6 | 63 & this.get(r++)) : String.fromCharCode((15 & o) << 12 | (63 & this.get(r++)) << 6 | 63 & this.get(r++))
                }
                return n
            }
            ,
            e.prototype.parseStringBMP = function(e, t) {
                for (var n, r, o = "", i = e; i < t; )
                    n = this.get(i++),
                    r = this.get(i++),
                    o += String.fromCharCode(n << 8 | r);
                return o
            }
            ,
            e.prototype.parseTime = function(e, t, n) {
                var r = this.parseStringISO(e, t)
                  , o = (n ? w : C).exec(r);
                return o ? (n && (o[1] = +o[1],
                o[1] += +o[1] < 70 ? 2e3 : 1900),
                r = o[1] + "-" + o[2] + "-" + o[3] + " " + o[4],
                o[5] && (r += ":" + o[5],
                o[6] && (r += ":" + o[6],
                o[7] && (r += "." + o[7]))),
                o[8] && (r += " UTC",
                "Z" != o[8] && (r += o[8],
                o[9] && (r += ":" + o[9]))),
                r) : "Unrecognized time: " + r
            }
            ,
            e.prototype.parseInteger = function(e, t) {
                var n, r = this.get(e), o = r > 127, i = o ? 255 : 0, s = "";
                while (r == i && ++e < t)
                    r = this.get(e);
                if (n = t - e,
                0 === n)
                    return o ? -1 : 0;
                if (n > 4) {
                    s = r,
                    n <<= 3;
                    while (0 == (128 & (+s ^ i)))
                        s = +s << 1,
                        --n;
                    s = "(" + n + " bit)\n"
                }
                o && (r -= 256);
                for (var a = new _(r), c = e + 1; c < t; ++c)
                    a.mulAdd(256, this.get(c));
                return s + a.toString()
            }
            ,
            e.prototype.parseBitString = function(e, t, n) {
                for (var r = this.get(e), o = (t - e - 1 << 3) - r, i = "(" + o + " bit)\n", s = "", a = e + 1; a < t; ++a) {
                    for (var c = this.get(a), l = a == t - 1 ? r : 0, u = 7; u >= l; --u)
                        s += c >> u & 1 ? "1" : "0";
                    if (s.length > n)
                        return i + j(s, n)
                }
                return i + s
            }
            ,
            e.prototype.parseOctetString = function(e, t, n) {
                if (this.isASCII(e, t))
                    return j(this.parseStringISO(e, t), n);
                var r = t - e
                  , o = "(" + r + " byte)\n";
                n /= 2,
                r > n && (t = e + n);
                for (var i = e; i < t; ++i)
                    o += this.hexByte(this.get(i));
                return r > n && (o += x),
                o
            }
            ,
            e.prototype.parseOID = function(e, t, n) {
                for (var r = "", o = new _, i = 0, s = e; s < t; ++s) {
                    var a = this.get(s);
                    if (o.mulAdd(128, 127 & a),
                    i += 7,
                    !(128 & a)) {
                        if ("" === r)
                            if (o = o.simplify(),
                            o instanceof _)
                                o.sub(80),
                                r = "2." + o.toString();
                            else {
                                var c = o < 80 ? o < 40 ? 0 : 1 : 2;
                                r = c + "." + (o - 40 * c)
                            }
                        else
                            r += "." + o.toString();
                        if (r.length > n)
                            return j(r, n);
                        o = new _,
                        i = 0
                    }
                }
                return i > 0 && (r += ".incomplete"),
                r
            }
            ,
            e
        }(),
    O = function() {
            function e(e, t, n, r, o) {
                if (!(r instanceof k))
                    throw new Error("Invalid tag value.");
                this.stream = e,
                this.header = t,
                this.length = n,
                this.tag = r,
                this.sub = o
            }
            return e.prototype.typeName = function() {
                switch (this.tag.tagClass) {
                case 0:
                    switch (this.tag.tagNumber) {
                    case 0:
                        return "EOC";
                    case 1:
                        return "BOOLEAN";
                    case 2:
                        return "INTEGER";
                    case 3:
                        return "BIT_STRING";
                    case 4:
                        return "OCTET_STRING";
                    case 5:
                        return "NULL";
                    case 6:
                        return "OBJECT_IDENTIFIER";
                    case 7:
                        return "ObjectDescriptor";
                    case 8:
                        return "EXTERNAL";
                    case 9:
                        return "REAL";
                    case 10:
                        return "ENUMERATED";
                    case 11:
                        return "EMBEDDED_PDV";
                    case 12:
                        return "UTF8String";
                    case 16:
                        return "SEQUENCE";
                    case 17:
                        return "SET";
                    case 18:
                        return "NumericString";
                    case 19:
                        return "PrintableString";
                    case 20:
                        return "TeletexString";
                    case 21:
                        return "VideotexString";
                    case 22:
                        return "IA5String";
                    case 23:
                        return "UTCTime";
                    case 24:
                        return "GeneralizedTime";
                    case 25:
                        return "GraphicString";
                    case 26:
                        return "VisibleString";
                    case 27:
                        return "GeneralString";
                    case 28:
                        return "UniversalString";
                    case 30:
                        return "BMPString"
                    }
                    return "Universal_" + this.tag.tagNumber.toString();
                case 1:
                    return "Application_" + this.tag.tagNumber.toString();
                case 2:
                    return "[" + this.tag.tagNumber.toString() + "]";
                case 3:
                    return "Private_" + this.tag.tagNumber.toString()
                }
            }
            ,
            e.prototype.content = function(e) {
                if (void 0 === this.tag)
                    return null;
                void 0 === e && (e = 1 / 0);
                var t = this.posContent()
                  , n = Math.abs(this.length);
                if (!this.tag.isUniversal())
                    return null !== this.sub ? "(" + this.sub.length + " elem)" : this.stream.parseOctetString(t, t + n, e);
                switch (this.tag.tagNumber) {
                case 1:
                    return 0 === this.stream.get(t) ? "false" : "true";
                case 2:
                    return this.stream.parseInteger(t, t + n);
                case 3:
                    return this.sub ? "(" + this.sub.length + " elem)" : this.stream.parseBitString(t, t + n, e);
                case 4:
                    return this.sub ? "(" + this.sub.length + " elem)" : this.stream.parseOctetString(t, t + n, e);
                case 6:
                    return this.stream.parseOID(t, t + n, e);
                case 16:
                case 17:
                    return null !== this.sub ? "(" + this.sub.length + " elem)" : "(no elem)";
                case 12:
                    return j(this.stream.parseStringUTF(t, t + n), e);
                case 18:
                case 19:
                case 20:
                case 21:
                case 22:
                case 26:
                    return j(this.stream.parseStringISO(t, t + n), e);
                case 30:
                    return j(this.stream.parseStringBMP(t, t + n), e);
                case 23:
                case 24:
                    return this.stream.parseTime(t, t + n, 23 == this.tag.tagNumber)
                }
                return null
            }
            ,
            e.prototype.toString = function() {
                return this.typeName() + "@" + this.stream.pos + "[header:" + this.header + ",length:" + this.length + ",sub:" + (null === this.sub ? "null" : this.sub.length) + "]"
            }
            ,
            e.prototype.toPrettyString = function(e) {
                void 0 === e && (e = "");
                var t = e + this.typeName() + " @" + this.stream.pos;
                if (this.length >= 0 && (t += "+"),
                t += this.length,
                this.tag.tagConstructed ? t += " (constructed)" : !this.tag.isUniversal() || 3 != this.tag.tagNumber && 4 != this.tag.tagNumber || null === this.sub || (t += " (encapsulates)"),
                t += "\n",
                null !== this.sub) {
                    e += "  ";
                    for (var n = 0, r = this.sub.length; n < r; ++n)
                        t += this.sub[n].toPrettyString(e)
                }
                return t
            }
            ,
            e.prototype.posStart = function() {
                return this.stream.pos
            }
            ,
            e.prototype.posContent = function() {
                return this.stream.pos + this.header
            }
            ,
            e.prototype.posEnd = function() {
                return this.stream.pos + this.header + Math.abs(this.length)
            }
            ,
            e.prototype.toHexString = function() {
                return this.stream.hexDump(this.posStart(), this.posEnd(), !0)
            }
            ,
            e.decodeLength = function(e) {
                var t = e.get()
                  , n = 127 & t;
                if (n == t)
                    return n;
                if (n > 6)
                    throw new Error("Length over 48 bits not supported at position " + (e.pos - 1));
                if (0 === n)
                    return null;
                t = 0;
                for (var r = 0; r < n; ++r)
                    t = 256 * t + e.get();
                return t
            }
            ,
            e.prototype.getHexStringValue = function() {
                var e = this.toHexString()
                  , t = 2 * this.header
                  , n = 2 * this.length;
                return e.substr(t, n)
            }
            ,
            e.decode = function(t) {
                var n;
                n = t instanceof M ? t : new M(t,0);
                var r = new M(n)
                  , o = new k(n)
                  , i = e.decodeLength(n)
                  , s = n.pos
                  , a = s - r.pos
                  , c = null
                  , l = function() {
                    var t = [];
                    if (null !== i) {
                        var r = s + i;
                        while (n.pos < r)
                            t[t.length] = e.decode(n);
                        if (n.pos != r)
                            throw new Error("Content size is not correct for container starting at offset " + s)
                    } else
                        try {
                            for (; ; ) {
                                var o = e.decode(n);
                                if (o.tag.isEOC())
                                    break;
                                t[t.length] = o
                            }
                            i = s - n.pos
                        } catch (a) {
                            throw new Error("Exception while decoding undefined length content: " + a)
                        }
                    return t
                };
                if (o.tagConstructed)
                    c = l();
                else if (o.isUniversal() && (3 == o.tagNumber || 4 == o.tagNumber))
                    try {
                        if (3 == o.tagNumber && 0 != n.get())
                            throw new Error("BIT STRINGs with unused bits cannot encapsulate.");
                        c = l();
                        for (var u = 0; u < c.length; ++u)
                            if (c[u].tag.isEOC())
                                throw new Error("EOC is not supposed to be actual content.")
                    } catch (d) {
                        c = null
                    }
                if (null === c) {
                    if (null === i)
                        throw new Error("We can't skip over an invalid tag with undefined length at offset " + s);
                    n.pos = s + Math.abs(i)
                }
                return new e(r,a,i,o,c)
            }
            ,
            e
        }(),
    k = function() {
            function e(e) {
                var t = e.get();
                if (this.tagClass = t >> 6,
                this.tagConstructed = 0 !== (32 & t),
                this.tagNumber = 31 & t,
                31 == this.tagNumber) {
                    var n = new _;
                    do {
                        t = e.get(),
                        n.mulAdd(128, 127 & t)
                    } while (128 & t);
                    this.tagNumber = n.simplify()
                }
            }
            return e.prototype.isUniversal = function() {
                return 0 === this.tagClass
            }
            ,
            e.prototype.isEOC = function() {
                return 0 === this.tagClass && 0 === this.tagNumber
            }
            ,
            e
        }(),
    T = 0xdeadbeefcafe,
    L = 15715070 == (16777215 & T),
    z = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997],
    P = (1 << 26) / z[z.length - 1],
    H = function() {
             function e(e, t, n) {
                null != e && ("number" == typeof e ? e.prototype.fromNumber(e, t, n) : null == t && "string" != typeof e ? this.fromString(e, 256) : this.fromString(e, t))
            }
            return e.prototype.toString = function(e) {
                if (this.s < 0)
                    return "-" + this.negate().toString(e);
                var t;
                if (16 == e)
                    t = 4;
                else if (8 == e)
                    t = 3;
                else if (2 == e)
                    t = 1;
                else if (32 == e)
                    t = 5;
                else {
                    if (4 != e)
                        return this.toRadix(e);
                    t = 2
                }
                var n, r = (1 << t) - 1, i = !1, s = "", a = this.t, c = this.DB - a * this.DB % t;
                if (a-- > 0) {
                    c < this.DB && (n = this[a] >> c) > 0 && (i = !0,
                    s = o(n));
                    while (a >= 0)
                        c < t ? (n = (this[a] & (1 << c) - 1) << t - c,
                        n |= this[--a] >> (c += this.DB - t)) : (n = this[a] >> (c -= t) & r,
                        c <= 0 && (c += this.DB,
                        --a)),
                        n > 0 && (i = !0),
                        i && (s += o(n))
                }
                return i ? s : "0"
            }
            ,
            e.prototype.negate = function() {
                var t = R();
                return e.ZERO.subTo(this, t),
                t
            }
            ,
            e.prototype.abs = function() {
                return this.s < 0 ? this.negate() : this
            }
            ,
            e.prototype.compareTo = function(e) {
                var t = this.s - e.s;
                if (0 != t)
                    return t;
                var n = this.t;
                if (t = n - e.t,
                0 != t)
                    return this.s < 0 ? -t : t;
                while (--n >= 0)
                    if (0 != (t = this[n] - e[n]))
                        return t;
                return 0
            }
            ,
            e.prototype.bitLength = function() {
                return this.t <= 0 ? 0 : this.DB * (this.t - 1) + U(this[this.t - 1] ^ this.s & this.DM)
            }
            ,
            e.prototype.mod = function(t) {
                var n = R();
                return this.abs().divRemTo(t, null, n),
                this.s < 0 && n.compareTo(e.ZERO) > 0 && t.subTo(n, n),
                n
            }
            ,
            e.prototype.modPowInt = function(e, t) {
                var n;
                return n = e < 256 || t.isEven() ? new D(t) : new V(t),
                this.exp(e, n)
            }
            ,
            e.prototype.clone = function() {
                var e = R();
                return this.copyTo(e),
                e
            }
            ,
            e.prototype.intValue = function() {
                if (this.s < 0) {
                    if (1 == this.t)
                        return this[0] - this.DV;
                    if (0 == this.t)
                        return -1
                } else {
                    if (1 == this.t)
                        return this[0];
                    if (0 == this.t)
                        return 0
                }
                return (this[1] & (1 << 32 - this.DB) - 1) << this.DB | this[0]
            }
            ,
            e.prototype.byteValue = function() {
                return 0 == this.t ? this.s : this[0] << 24 >> 24
            }
            ,
            e.prototype.shortValue = function() {
                return 0 == this.t ? this.s : this[0] << 16 >> 16
            }
            ,
            e.prototype.signum = function() {
                return this.s < 0 ? -1 : this.t <= 0 || 1 == this.t && this[0] <= 0 ? 0 : 1
            }
            ,
            e.prototype.toByteArray = function() {
                var e = this.t
                  , t = [];
                t[0] = this.s;
                var n, r = this.DB - e * this.DB % 8, o = 0;
                if (e-- > 0) {
                    r < this.DB && (n = this[e] >> r) != (this.s & this.DM) >> r && (t[o++] = n | this.s << this.DB - r);
                    while (e >= 0)
                        r < 8 ? (n = (this[e] & (1 << r) - 1) << 8 - r,
                        n |= this[--e] >> (r += this.DB - 8)) : (n = this[e] >> (r -= 8) & 255,
                        r <= 0 && (r += this.DB,
                        --e)),
                        0 != (128 & n) && (n |= -256),
                        0 == o && (128 & this.s) != (128 & n) && ++o,
                        (o > 0 || n != this.s) && (t[o++] = n)
                }
                return t
            }
            ,
            e.prototype.equals = function(e) {
                return 0 == this.compareTo(e)
            }
            ,
            e.prototype.min = function(e) {
                return this.compareTo(e) < 0 ? this : e
            }
            ,
            e.prototype.max = function(e) {
                return this.compareTo(e) > 0 ? this : e
            }
            ,
            e.prototype.and = function(e) {
                var t = R();
                return this.bitwiseTo(e, i, t),
                t
            }
            ,
            e.prototype.or = function(e) {
                var t = R();
                return this.bitwiseTo(e, s, t),
                t
            }
            ,
            e.prototype.xor = function(e) {
                var t = R();
                return this.bitwiseTo(e, a, t),
                t
            }
            ,
            e.prototype.andNot = function(e) {
                var t = R();
                return this.bitwiseTo(e, c, t),
                t
            }
            ,
            e.prototype.not = function() {
                for (var e = R(), t = 0; t < this.t; ++t)
                    e[t] = this.DM & ~this[t];
                return e.t = this.t,
                e.s = ~this.s,
                e
            }
            ,
            e.prototype.shiftLeft = function(e) {
                var t = R();
                return e < 0 ? this.rShiftTo(-e, t) : this.lShiftTo(e, t),
                t
            }
            ,
            e.prototype.shiftRight = function(e) {
                var t = R();
                return e < 0 ? this.lShiftTo(-e, t) : this.rShiftTo(e, t),
                t
            }
            ,
            e.prototype.getLowestSetBit = function() {
                for (var e = 0; e < this.t; ++e)
                    if (0 != this[e])
                        return e * this.DB + l(this[e]);
                return this.s < 0 ? this.t * this.DB : -1
            }
            ,
            e.prototype.bitCount = function() {
                for (var e = 0, t = this.s & this.DM, n = 0; n < this.t; ++n)
                    e += u(this[n] ^ t);
                return e
            }
            ,
            e.prototype.testBit = function(e) {
                var t = Math.floor(e / this.DB);
                return t >= this.t ? 0 != this.s : 0 != (this[t] & 1 << e % this.DB)
            }
            ,
            e.prototype.setBit = function(e) {
                return this.changeBit(e, s)
            }
            ,
            e.prototype.clearBit = function(e) {
                return this.changeBit(e, c)
            }
            ,
            e.prototype.flipBit = function(e) {
                return this.changeBit(e, a)
            }
            ,
            e.prototype.add = function(e) {
                var t = R();
                return this.addTo(e, t),
                t
            }
            ,
            e.prototype.subtract = function(e) {
                var t = R();
                return this.subTo(e, t),
                t
            }
            ,
            e.prototype.multiply = function(e) {
                var t = R();
                return this.multiplyTo(e, t),
                t
            }
            ,
            e.prototype.divide = function(e) {
                var t = R();
                return this.divRemTo(e, t, null),
                t
            }
            ,
            e.prototype.remainder = function(e) {
                var t = R();
                return this.divRemTo(e, null, t),
                t
            }
            ,
            e.prototype.divideAndRemainder = function(e) {
                var t = R()
                  , n = R();
                return this.divRemTo(e, t, n),
                [t, n]
            }
            ,
            e.prototype.modPow = function(e, t) {
                var n, r, o = e.bitLength(), i = W(1);
                if (o <= 0)
                    return i;
                n = o < 18 ? 1 : o < 48 ? 3 : o < 144 ? 4 : o < 768 ? 5 : 6,
                r = o < 8 ? new D(t) : t.isEven() ? new A(t) : new V(t);
                var s = []
                  , a = 3
                  , c = n - 1
                  , l = (1 << n) - 1;
                if (s[1] = r.convert(this),
                n > 1) {
                    var u = R();
                    r.sqrTo(s[1], u);
                    while (a <= l)
                        s[a] = R(),
                        r.mulTo(u, s[a - 2], s[a]),
                        a += 2
                }
                var d, f, h = e.t - 1, p = !0, m = R();
                o = U(e[h]) - 1;
                while (h >= 0) {
                    o >= c ? d = e[h] >> o - c & l : (d = (e[h] & (1 << o + 1) - 1) << c - o,
                    h > 0 && (d |= e[h - 1] >> this.DB + o - c)),
                    a = n;
                    while (0 == (1 & d))
                        d >>= 1,
                        --a;
                    if ((o -= a) < 0 && (o += this.DB,
                    --h),
                    p)
                        s[d].copyTo(i),
                        p = !1;
                    else {
                        while (a > 1)
                            r.sqrTo(i, m),
                            r.sqrTo(m, i),
                            a -= 2;
                        a > 0 ? r.sqrTo(i, m) : (f = i,
                        i = m,
                        m = f),
                        r.mulTo(m, s[d], i)
                    }
                    while (h >= 0 && 0 == (e[h] & 1 << o))
                        r.sqrTo(i, m),
                        f = i,
                        i = m,
                        m = f,
                        --o < 0 && (o = this.DB - 1,
                        --h)
                }
                return r.revert(i)
            }
            ,
            e.prototype.modInverse = function(t) {
                var n = t.isEven();
                if (this.isEven() && n || 0 == t.signum())
                    return e.ZERO;
                var r = t.clone()
                  , o = this.clone()
                  , i = W(1)
                  , s = W(0)
                  , a = W(0)
                  , c = W(1);
                while (0 != r.signum()) {
                    while (r.isEven())
                        r.rShiftTo(1, r),
                        n ? (i.isEven() && s.isEven() || (i.addTo(this, i),
                        s.subTo(t, s)),
                        i.rShiftTo(1, i)) : s.isEven() || s.subTo(t, s),
                        s.rShiftTo(1, s);
                    while (o.isEven())
                        o.rShiftTo(1, o),
                        n ? (a.isEven() && c.isEven() || (a.addTo(this, a),
                        c.subTo(t, c)),
                        a.rShiftTo(1, a)) : c.isEven() || c.subTo(t, c),
                        c.rShiftTo(1, c);
                    r.compareTo(o) >= 0 ? (r.subTo(o, r),
                    n && i.subTo(a, i),
                    s.subTo(c, s)) : (o.subTo(r, o),
                    n && a.subTo(i, a),
                    c.subTo(s, c))
                }
                return 0 != o.compareTo(e.ONE) ? e.ZERO : c.compareTo(t) >= 0 ? c.subtract(t) : c.signum() < 0 ? (c.addTo(t, c),
                c.signum() < 0 ? c.add(t) : c) : c
            }
            ,
            e.prototype.pow = function(e) {
                return this.exp(e, new E)
            }
            ,
            e.prototype.gcd = function(e) {
                var t = this.s < 0 ? this.negate() : this.clone()
                  , n = e.s < 0 ? e.negate() : e.clone();
                if (t.compareTo(n) < 0) {
                    var r = t;
                    t = n,
                    n = r
                }
                var o = t.getLowestSetBit()
                  , i = n.getLowestSetBit();
                if (i < 0)
                    return t;
                o < i && (i = o),
                i > 0 && (t.rShiftTo(i, t),
                n.rShiftTo(i, n));
                while (t.signum() > 0)
                    (o = t.getLowestSetBit()) > 0 && t.rShiftTo(o, t),
                    (o = n.getLowestSetBit()) > 0 && n.rShiftTo(o, n),
                    t.compareTo(n) >= 0 ? (t.subTo(n, t),
                    t.rShiftTo(1, t)) : (n.subTo(t, n),
                    n.rShiftTo(1, n));
                return i > 0 && n.lShiftTo(i, n),
                n
            }
            ,
            e.prototype.isProbablePrime = function(e) {
                var t, n = this.abs();
                if (1 == n.t && n[0] <= z[z.length - 1]) {
                    for (t = 0; t < z.length; ++t)
                        if (n[0] == z[t])
                            return !0;
                    return !1
                }
                if (n.isEven())
                    return !1;
                t = 1;
                while (t < z.length) {
                    var r = z[t]
                      , o = t + 1;
                    while (o < z.length && r < P)
                        r *= z[o++];
                    r = n.modInt(r);
                    while (t < o)
                        if (r % z[t++] == 0)
                            return !1
                }
                return n.millerRabin(e)
            }
            ,
            e.prototype.copyTo = function(e) {
                for (var t = this.t - 1; t >= 0; --t)
                    e[t] = this[t];
                e.t = this.t,
                e.s = this.s
            }
            ,
            e.prototype.fromInt = function(e) {
                this.t = 1,
                this.s = e < 0 ? -1 : 0,
                e > 0 ? this[0] = e : e < -1 ? this[0] = e + this.DV : this.t = 0
            }
            ,
            e.prototype.fromString = function(t, n) {
                var r;
                if (16 == n)
                    r = 4;
                else if (8 == n)
                    r = 3;
                else if (256 == n)
                    r = 8;
                else if (2 == n)
                    r = 1;
                else if (32 == n)
                    r = 5;
                else {
                    if (4 != n)
                        return void this.fromRadix(t, n);
                    r = 2
                }
                this.t = 0,
                this.s = 0;
                var o = t.length
                  , i = !1
                  , s = 0;
                while (--o >= 0) {
                    var a = 8 == r ? 255 & +t[o] : K(t, o);
                    a < 0 ? "-" == t.charAt(o) && (i = !0) : (i = !1,
                    0 == s ? this[this.t++] = a : s + r > this.DB ? (this[this.t - 1] |= (a & (1 << this.DB - s) - 1) << s,
                    this[this.t++] = a >> this.DB - s) : this[this.t - 1] |= a << s,
                    s += r,
                    s >= this.DB && (s -= this.DB))
                }
                8 == r && 0 != (128 & +t[0]) && (this.s = -1,
                s > 0 && (this[this.t - 1] |= (1 << this.DB - s) - 1 << s)),
                this.clamp(),
                i && e.ZERO.subTo(this, this)
            }
            ,
            e.prototype.clamp = function() {
                var e = this.s & this.DM;
                while (this.t > 0 && this[this.t - 1] == e)
                    --this.t
            }
            ,
            e.prototype.dlShiftTo = function(e, t) {
                var n;
                for (n = this.t - 1; n >= 0; --n)
                    t[n + e] = this[n];
                for (n = e - 1; n >= 0; --n)
                    t[n] = 0;
                t.t = this.t + e,
                t.s = this.s
            }
            ,
            e.prototype.drShiftTo = function(e, t) {
                for (var n = e; n < this.t; ++n)
                    t[n - e] = this[n];
                t.t = Math.max(this.t - e, 0),
                t.s = this.s
            }
            ,
            e.prototype.lShiftTo = function(e, t) {
                for (var n = e % this.DB, r = this.DB - n, o = (1 << r) - 1, i = Math.floor(e / this.DB), s = this.s << n & this.DM, a = this.t - 1; a >= 0; --a)
                    t[a + i + 1] = this[a] >> r | s,
                    s = (this[a] & o) << n;
                for (a = i - 1; a >= 0; --a)
                    t[a] = 0;
                t[i] = s,
                t.t = this.t + i + 1,
                t.s = this.s,
                t.clamp()
            }
            ,
            e.prototype.rShiftTo = function(e, t) {
                t.s = this.s;
                var n = Math.floor(e / this.DB);
                if (n >= this.t)
                    t.t = 0;
                else {
                    var r = e % this.DB
                      , o = this.DB - r
                      , i = (1 << r) - 1;
                    t[0] = this[n] >> r;
                    for (var s = n + 1; s < this.t; ++s)
                        t[s - n - 1] |= (this[s] & i) << o,
                        t[s - n] = this[s] >> r;
                    r > 0 && (t[this.t - n - 1] |= (this.s & i) << o),
                    t.t = this.t - n,
                    t.clamp()
                }
            }
            ,
            e.prototype.subTo = function(e, t) {
                var n = 0
                  , r = 0
                  , o = Math.min(e.t, this.t);
                while (n < o)
                    r += this[n] - e[n],
                    t[n++] = r & this.DM,
                    r >>= this.DB;
                if (e.t < this.t) {
                    r -= e.s;
                    while (n < this.t)
                        r += this[n],
                        t[n++] = r & this.DM,
                        r >>= this.DB;
                    r += this.s
                } else {
                    r += this.s;
                    while (n < e.t)
                        r -= e[n],
                        t[n++] = r & this.DM,
                        r >>= this.DB;
                    r -= e.s
                }
                t.s = r < 0 ? -1 : 0,
                r < -1 ? t[n++] = this.DV + r : r > 0 && (t[n++] = r),
                t.t = n,
                t.clamp()
            }
            ,
            e.prototype.multiplyTo = function(t, n) {
                var r = this.abs()
                  , o = t.abs()
                  , i = r.t;
                n.t = i + o.t;
                while (--i >= 0)
                    n[i] = 0;
                for (i = 0; i < o.t; ++i)
                    n[i + r.t] = r.am(0, o[i], n, i, 0, r.t);
                n.s = 0,
                n.clamp(),
                this.s != t.s && e.ZERO.subTo(n, n)
            }
            ,
            e.prototype.squareTo = function(e) {
                var t = this.abs()
                  , n = e.t = 2 * t.t;
                while (--n >= 0)
                    e[n] = 0;
                for (n = 0; n < t.t - 1; ++n) {
                    var r = t.am(n, t[n], e, 2 * n, 0, 1);
                    (e[n + t.t] += t.am(n + 1, 2 * t[n], e, 2 * n + 1, r, t.t - n - 1)) >= t.DV && (e[n + t.t] -= t.DV,
                    e[n + t.t + 1] = 1)
                }
                e.t > 0 && (e[e.t - 1] += t.am(n, t[n], e, 2 * n, 0, 1)),
                e.s = 0,
                e.clamp()
            }
            ,
            e.prototype.divRemTo = function(t, n, r) {
                var o = t.abs();
                if (!(o.t <= 0)) {
                    var i = this.abs();
                    if (i.t < o.t)
                        return null != n && n.fromInt(0),
                        void (null != r && this.copyTo(r));
                    null == r && (r = R());
                    var s = R()
                      , a = this.s
                      , c = t.s
                      , l = this.DB - U(o[o.t - 1]);
                    l > 0 ? (o.lShiftTo(l, s),
                    i.lShiftTo(l, r)) : (o.copyTo(s),
                    i.copyTo(r));
                    var u = s.t
                      , d = s[u - 1];
                    if (0 != d) {
                        var f = d * (1 << this.F1) + (u > 1 ? s[u - 2] >> this.F2 : 0)
                          , h = this.FV / f
                          , p = (1 << this.F1) / f
                          , m = 1 << this.F2
                          , v = r.t
                          , b = v - u
                          , g = null == n ? R() : n;
                        s.dlShiftTo(b, g),
                        r.compareTo(g) >= 0 && (r[r.t++] = 1,
                        r.subTo(g, r)),
                        e.ONE.dlShiftTo(u, g),
                        g.subTo(s, s);
                        while (s.t < u)
                            s[s.t++] = 0;
                        while (--b >= 0) {
                            var y = r[--v] == d ? this.DM : Math.floor(r[v] * h + (r[v - 1] + m) * p);
                            if ((r[v] += s.am(0, y, r, b, 0, u)) < y) {
                                s.dlShiftTo(b, g),
                                r.subTo(g, r);
                                while (r[v] < --y)
                                    r.subTo(g, r)
                            }
                        }
                        null != n && (r.drShiftTo(u, n),
                        a != c && e.ZERO.subTo(n, n)),
                        r.t = u,
                        r.clamp(),
                        l > 0 && r.rShiftTo(l, r),
                        a < 0 && e.ZERO.subTo(r, r)
                    }
                }
            }
            ,
            e.prototype.invDigit = function() {
                if (this.t < 1)
                    return 0;
                var e = this[0];
                if (0 == (1 & e))
                    return 0;
                var t = 3 & e;
                return t = t * (2 - (15 & e) * t) & 15,
                t = t * (2 - (255 & e) * t) & 255,
                t = t * (2 - ((65535 & e) * t & 65535)) & 65535,
                t = t * (2 - e * t % this.DV) % this.DV,
                t > 0 ? this.DV - t : -t
            }
            ,
            e.prototype.isEven = function() {
                return 0 == (this.t > 0 ? 1 & this[0] : this.s)
            }
            ,
            e.prototype.exp = function(t, n) {
                if (t > 4294967295 || t < 1)
                    return e.ONE;
                var r = R()
                  , o = R()
                  , i = n.convert(this)
                  , s = U(t) - 1;
                i.copyTo(r);
                while (--s >= 0)
                    if (n.sqrTo(r, o),
                    (t & 1 << s) > 0)
                        n.mulTo(o, i, r);
                    else {
                        var a = r;
                        r = o,
                        o = a
                    }
                return n.revert(r)
            }
            ,
            e.prototype.chunkSize = function(e) {
                return Math.floor(Math.LN2 * this.DB / Math.log(e))
            }
            ,
            e.prototype.toRadix = function(e) {
                if (null == e && (e = 10),
                0 == this.signum() || e < 2 || e > 36)
                    return "0";
                var t = this.chunkSize(e)
                  , n = Math.pow(e, t)
                  , r = W(n)
                  , o = R()
                  , i = R()
                  , s = "";
                this.divRemTo(r, o, i);
                while (o.signum() > 0)
                    s = (n + i.intValue()).toString(e).substr(1) + s,
                    o.divRemTo(r, o, i);
                return i.intValue().toString(e) + s
            }
            ,
            e.prototype.fromRadix = function(t, n) {
                this.fromInt(0),
                null == n && (n = 10);
                for (var r = this.chunkSize(n), o = Math.pow(n, r), i = !1, s = 0, a = 0, c = 0; c < t.length; ++c) {
                    var l = K(t, c);
                    l < 0 ? "-" == t.charAt(c) && 0 == this.signum() && (i = !0) : (a = n * a + l,
                    ++s >= r && (this.dMultiply(o),
                    this.dAddOffset(a, 0),
                    s = 0,
                    a = 0))
                }
                s > 0 && (this.dMultiply(Math.pow(n, s)),
                this.dAddOffset(a, 0)),
                i && e.ZERO.subTo(this, this)
            }
            ,
            e.prototype.fromNumber = function(t, n, r) {
                if ("number" == typeof n)
                    if (t < 2)
                        this.fromInt(1);
                    else {
                        this.fromNumber(t, r),
                        this.testBit(t - 1) || this.bitwiseTo(e.ONE.shiftLeft(t - 1), s, this),
                        this.isEven() && this.dAddOffset(1, 0);
                        while (!this.isProbablePrime(n))
                            this.dAddOffset(2, 0),
                            this.bitLength() > t && this.subTo(e.ONE.shiftLeft(t - 1), this)
                    }
                else {
                    var o = []
                      , i = 7 & t;
                    o.length = 1 + (t >> 3),
                    n.nextBytes(o),
                    i > 0 ? o[0] &= (1 << i) - 1 : o[0] = 0,
                    this.fromString(o, 256)
                }
            }
            ,
            e.prototype.bitwiseTo = function(e, t, n) {
                var r, o, i = Math.min(e.t, this.t);
                for (r = 0; r < i; ++r)
                    n[r] = t(this[r], e[r]);
                if (e.t < this.t) {
                    for (o = e.s & this.DM,
                    r = i; r < this.t; ++r)
                        n[r] = t(this[r], o);
                    n.t = this.t
                } else {
                    for (o = this.s & this.DM,
                    r = i; r < e.t; ++r)
                        n[r] = t(o, e[r]);
                    n.t = e.t
                }
                n.s = t(this.s, e.s),
                n.clamp()
            }
            ,
            e.prototype.changeBit = function(t, n) {
                var r = e.ONE.shiftLeft(t);
                return this.bitwiseTo(r, n, r),
                r
            }
            ,
            e.prototype.addTo = function(e, t) {
                var n = 0
                  , r = 0
                  , o = Math.min(e.t, this.t);
                while (n < o)
                    r += this[n] + e[n],
                    t[n++] = r & this.DM,
                    r >>= this.DB;
                if (e.t < this.t) {
                    r += e.s;
                    while (n < this.t)
                        r += this[n],
                        t[n++] = r & this.DM,
                        r >>= this.DB;
                    r += this.s
                } else {
                    r += this.s;
                    while (n < e.t)
                        r += e[n],
                        t[n++] = r & this.DM,
                        r >>= this.DB;
                    r += e.s
                }
                t.s = r < 0 ? -1 : 0,
                r > 0 ? t[n++] = r : r < -1 && (t[n++] = this.DV + r),
                t.t = n,
                t.clamp()
            }
            ,
            e.prototype.dMultiply = function(e) {
                this[this.t] = this.am(0, e - 1, this, 0, 0, this.t),
                ++this.t,
                this.clamp()
            }
            ,
            e.prototype.dAddOffset = function(e, t) {
                if (0 != e) {
                    while (this.t <= t)
                        this[this.t++] = 0;
                    this[t] += e;
                    while (this[t] >= this.DV)
                        this[t] -= this.DV,
                        ++t >= this.t && (this[this.t++] = 0),
                        ++this[t]
                }
            }
            ,
            e.prototype.multiplyLowerTo = function(e, t, n) {
                var r = Math.min(this.t + e.t, t);
                n.s = 0,
                n.t = r;
                while (r > 0)
                    n[--r] = 0;
                for (var o = n.t - this.t; r < o; ++r)
                    n[r + this.t] = this.am(0, e[r], n, r, 0, this.t);
                for (o = Math.min(e.t, t); r < o; ++r)
                    this.am(0, e[r], n, r, 0, t - r);
                n.clamp()
            }
            ,
            e.prototype.multiplyUpperTo = function(e, t, n) {
                --t;
                var r = n.t = this.t + e.t - t;
                n.s = 0;
                while (--r >= 0)
                    n[r] = 0;
                for (r = Math.max(t - this.t, 0); r < e.t; ++r)
                    n[this.t + r - t] = this.am(t - r, e[r], n, 0, 0, this.t + r - t);
                n.clamp(),
                n.drShiftTo(1, n)
            }
            ,
            e.prototype.modInt = function(e) {
                if (e <= 0)
                    return 0;
                var t = this.DV % e
                  , n = this.s < 0 ? e - 1 : 0;
                if (this.t > 0)
                    if (0 == t)
                        n = this[0] % e;
                    else
                        for (var r = this.t - 1; r >= 0; --r)
                            n = (t * n + this[r]) % e;
                return n
            }
            ,
            e.prototype.millerRabin = function(t) {
                var n = this.subtract(e.ONE)
                  , r = n.getLowestSetBit();
                if (r <= 0)
                    return !1;
                var o = n.shiftRight(r);
                t = t + 1 >> 1,
                t > z.length && (t = z.length);
                for (var i = R(), s = 0; s < t; ++s) {
                    i.fromInt(z[Math.floor(Math.random() * z.length)]);
                    var a = i.modPow(o, this);
                    if (0 != a.compareTo(e.ONE) && 0 != a.compareTo(n)) {
                        var c = 1;
                        while (c++ < r && 0 != a.compareTo(n))
                            if (a = a.modPowInt(2, this),
                            0 == a.compareTo(e.ONE))
                                return !1;
                        if (0 != a.compareTo(n))
                            return !1
                    }
                }
                return !0
            }
            ,
            e.prototype.square = function() {
                var e = R();
                return this.squareTo(e),
                e
            }
            ,
            e.prototype.gcda = function(e, t) {
                var n = this.s < 0 ? this.negate() : this.clone()
                  , r = e.s < 0 ? e.negate() : e.clone();
                if (n.compareTo(r) < 0) {
                    var o = n;
                    n = r,
                    r = o
                }
                var i = n.getLowestSetBit()
                  , s = r.getLowestSetBit();
                if (s < 0)
                    t(n);
                else {
                    i < s && (s = i),
                    s > 0 && (n.rShiftTo(s, n),
                    r.rShiftTo(s, r));
                    var a = function() {
                        (i = n.getLowestSetBit()) > 0 && n.rShiftTo(i, n),
                        (i = r.getLowestSetBit()) > 0 && r.rShiftTo(i, r),
                        n.compareTo(r) >= 0 ? (n.subTo(r, n),
                        n.rShiftTo(1, n)) : (r.subTo(n, r),
                        r.rShiftTo(1, r)),
                        n.signum() > 0 ? setTimeout(a, 0) : (s > 0 && r.lShiftTo(s, r),
                        setTimeout((function() {
                            t(r)
                        }
                        ), 0))
                    };
                    setTimeout(a, 10)
                }
            }
            ,
            e.prototype.fromNumberAsync = function(t, n, r, o) {
                if ("number" == typeof n)
                    if (t < 2)
                        this.fromInt(1);
                    else {
                        this.fromNumber(t, r),
                        this.testBit(t - 1) || this.bitwiseTo(e.ONE.shiftLeft(t - 1), s, this),
                        this.isEven() && this.dAddOffset(1, 0);
                        var i = this
                          , a = function() {
                            i.dAddOffset(2, 0),
                            i.bitLength() > t && i.subTo(e.ONE.shiftLeft(t - 1), i),
                            i.isProbablePrime(n) ? setTimeout((function() {
                                o()
                            }
                            ), 0) : setTimeout(a, 0)
                        };
                        setTimeout(a, 0)
                    }
                else {
                    var c = []
                      , l = 7 & t;
                    c.length = 1 + (t >> 3),
                    n.nextBytes(c),
                    l > 0 ? c[0] &= (1 << l) - 1 : c[0] = 0,
                    this.fromString(c, 256)
                }
            }
            ,
            e
        }()
    function F(e, t) {
        return new H(e,t)}
    var N, Y, B = [];
    for (N = "0".charCodeAt(0),
    Y = 0; Y <= 9; ++Y)
        B[N++] = Y;
    for (N = "a".charCodeAt(0),
    Y = 10; Y < 36; ++Y)
        B[N++] = Y;
    for (N = "A".charCodeAt(0),
    Y = 10; Y < 36; ++Y)
        B[N++] = Y;
    function K(e, t) {
            var n = B[e.charCodeAt(t)];
            return null == n ? -1 : n
        }
function oe() {
            if (null == X) {
                X = G();
                while (J < Z) {
                    var e = Math.floor(65536 * Math.random());
                    Q[J++] = 255 & e
                }
                for (X.init(Q),
                J = 0; J < Q.length; ++J)
                    Q[J] = 0;
                J = 0
            }
            return X.next()
        }
var ie = function() {
            function e() {}
            return e.prototype.nextBytes = function(e) {
                for (var t = 0; t < e.length; ++t)
                    e[t] = oe()
            }
            ,
            e
        }();
var ce = function() {
            function e() {
                this.n = null,
                this.e = 0,
                this.d = null,
                this.p = null,
                this.q = null,
                this.dmp1 = null,
                this.dmq1 = null,
                this.coeff = null
            }
            return e.prototype.doPublic = function(e) {
                return e.modPowInt(this.e, this.n)
            }
            ,
            e.prototype.doPrivate = function(e) {
                if (null == this.p || null == this.q)
                    return e.modPow(this.d, this.n);
                var t = e.mod(this.p).modPow(this.dmp1, this.p)
                  , n = e.mod(this.q).modPow(this.dmq1, this.q);
                while (t.compareTo(n) < 0)
                    t = t.add(this.p);
                return t.subtract(n).multiply(this.coeff).mod(this.p).multiply(this.q).add(n)
            }
            ,
            e.prototype.setPublic = function(e, t) {
                null != e && null != t && e.length > 0 && t.length > 0 ? (this.n = F(e, 16),
                this.e = parseInt(t, 16)) : console.error("Invalid RSA public key")
            }
            ,
            e.prototype.encrypt = function(e) {
                var t = this.n.bitLength() + 7 >> 3
                  , n = ae(e, t);
                if (null == n)
                    return null;
                var r = this.doPublic(n);
                if (null == r)
                    return null;
                for (var o = r.toString(16), i = o.length, s = 0; s < 2 * t - i; s++)
                    o = "0" + o;
                return o
            }
            ,
            e.prototype.setPrivate = function(e, t, n) {
                null != e && null != t && e.length > 0 && t.length > 0 ? (this.n = F(e, 16),
                this.e = parseInt(t, 16),
                this.d = F(n, 16)) : console.error("Invalid RSA private key")
            }
            ,
            e.prototype.setPrivateEx = function(e, t, n, r, o, i, s, a) {
                null != e && null != t && e.length > 0 && t.length > 0 ? (this.n = F(e, 16),
                this.e = parseInt(t, 16),
                this.d = F(n, 16),
                this.p = F(r, 16),
                this.q = F(o, 16),
                this.dmp1 = F(i, 16),
                this.dmq1 = F(s, 16),
                this.coeff = F(a, 16)) : console.error("Invalid RSA private key")
            }
            ,
            e.prototype.generate = function(e, t) {
                var n = new ie
                  , r = e >> 1;
                this.e = parseInt(t, 16);
                for (var o = new H(t,16); ; ) {
                    for (; ; )
                        if (this.p = new H(e - r,1,n),
                        0 == this.p.subtract(H.ONE).gcd(o).compareTo(H.ONE) && this.p.isProbablePrime(10))
                            break;
                    for (; ; )
                        if (this.q = new H(r,1,n),
                        0 == this.q.subtract(H.ONE).gcd(o).compareTo(H.ONE) && this.q.isProbablePrime(10))
                            break;
                    if (this.p.compareTo(this.q) <= 0) {
                        var i = this.p;
                        this.p = this.q,
                        this.q = i
                    }
                    var s = this.p.subtract(H.ONE)
                      , a = this.q.subtract(H.ONE)
                      , c = s.multiply(a);
                    if (0 == c.gcd(o).compareTo(H.ONE)) {
                        this.n = this.p.multiply(this.q),
                        this.d = o.modInverse(c),
                        this.dmp1 = this.d.mod(s),
                        this.dmq1 = this.d.mod(a),
                        this.coeff = this.q.modInverse(this.p);
                        break
                    }
                }
            }
            ,
            e.prototype.decrypt = function(e) {
                var t = F(e, 16)
                  , n = this.doPrivate(t);
                return null == n ? null : le(n, this.n.bitLength() + 7 >> 3)
            }
            ,
            e.prototype.generateAsync = function(e, t, n) {
                var r = new ie
                  , o = e >> 1;
                this.e = parseInt(t, 16);
                var i = new H(t,16)
                  , s = this
                  , a = function() {
                    var t = function() {
                        if (s.p.compareTo(s.q) <= 0) {
                            var e = s.p;
                            s.p = s.q,
                            s.q = e
                        }
                        var t = s.p.subtract(H.ONE)
                          , r = s.q.subtract(H.ONE)
                          , o = t.multiply(r);
                        0 == o.gcd(i).compareTo(H.ONE) ? (s.n = s.p.multiply(s.q),
                        s.d = i.modInverse(o),
                        s.dmp1 = s.d.mod(t),
                        s.dmq1 = s.d.mod(r),
                        s.coeff = s.q.modInverse(s.p),
                        setTimeout((function() {
                            n()
                        }
                        ), 0)) : setTimeout(a, 0)
                    }
                      , c = function() {
                        s.q = R(),
                        s.q.fromNumberAsync(o, 1, r, (function() {
                            s.q.subtract(H.ONE).gcda(i, (function(e) {
                                0 == e.compareTo(H.ONE) && s.q.isProbablePrime(10) ? setTimeout(t, 0) : setTimeout(c, 0)
                            }
                            ))
                        }
                        ))
                    }
                      , l = function() {
                        s.p = R(),
                        s.p.fromNumberAsync(e - o, 1, r, (function() {
                            s.p.subtract(H.ONE).gcda(i, (function(e) {
                                0 == e.compareTo(H.ONE) && s.p.isProbablePrime(10) ? setTimeout(c, 0) : setTimeout(l, 0)
                            }
                            ))
                        }
                        ))
                    };
                    setTimeout(l, 0)
                };
                setTimeout(a, 0)
            }
            ,
            e.prototype.sign = function(e, t, n) {
                var r = de(n)
                  , o = r + t(e).toString()
                  , i = se(o, this.n.bitLength() / 4);
                if (null == i)
                    return null;
                var s = this.doPrivate(i);
                if (null == s)
                    return null;
                var a = s.toString(16);
                return 0 == (1 & a.length) ? a : "0" + a
            }
            ,
            e.prototype.verify = function(e, t, n) {
                var r = F(t, 16)
                  , o = this.doPublic(r);
                if (null == o)
                    return null;
                var i = o.toString(16).replace(/^1f+00/, "")
                  , s = fe(i);
                return s == n(e).toString()
            }
            ,
            e
        }();
var me = function() {
            var e = function(t, n) {
                return e = Object.setPrototypeOf || {
                    __proto__: []
                }instanceof Array && function(e, t) {
                    e.__proto__ = t
                }
                || function(e, t) {
                    for (var n in t)
                        Object.prototype.hasOwnProperty.call(t, n) && (e[n] = t[n])
                }
                ,
                e(t, n)
            };
            return function(t, n) {
                if ("function" !== typeof n && null !== n)
                    throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
                function r() {
                    this.constructor = t
                }
                // e(t, n),
                t.prototype = null === n ? Object.create(n) : (r.prototype = n.prototype,
                new r)
            }
        }(),
    ve = function(e) {
            function t(n) {
                var r = e.call(this) || this;
                return n && ("string" === typeof n ? r.parseKey(n) : (t.hasPrivateKeyProperty(n) || t.hasPublicKeyProperty(n)) && r.parsePropertiesFrom(n)),
                r
            }
            return me(t, e),
            t.prototype.parseKey = function(e) {
                try {
                    var t = 0
                      , n = 0
                      , r = /^\s*(?:[0-9A-Fa-f][0-9A-Fa-f]\s*)+$/
                      , o = r.test(e) ? b.decode(e) : g.unarmor(e)
                      , i = O.decode(o);
                    if (3 === i.sub.length && (i = i.sub[2].sub[0]),
                    9 === i.sub.length) {
                        t = i.sub[1].getHexStringValue(),
                        this.n = F(t, 16),
                        n = i.sub[2].getHexStringValue(),
                        this.e = parseInt(n, 16);
                        var s = i.sub[3].getHexStringValue();
                        this.d = F(s, 16);
                        var a = i.sub[4].getHexStringValue();
                        this.p = F(a, 16);
                        var c = i.sub[5].getHexStringValue();
                        this.q = F(c, 16);
                        var l = i.sub[6].getHexStringValue();
                        this.dmp1 = F(l, 16);
                        var u = i.sub[7].getHexStringValue();
                        this.dmq1 = F(u, 16);
                        var d = i.sub[8].getHexStringValue();
                        this.coeff = F(d, 16)
                    } else {
                        if (2 !== i.sub.length)
                            return !1;
                        var f = i.sub[1]
                          , h = f.sub[0];
                        t = h.sub[0].getHexStringValue(),
                        this.n = F(t, 16),
                        n = h.sub[1].getHexStringValue(),
                        this.e = parseInt(n, 16)
                    }
                    return !0
                } catch (p) {
                    return !1
                }
            }
            ,
            t.prototype.getPrivateBaseKey = function() {
                var e = {
                    array: [new pe.asn1.DERInteger({
                        int: 0
                    }), new pe.asn1.DERInteger({
                        bigint: this.n
                    }), new pe.asn1.DERInteger({
                        int: this.e
                    }), new pe.asn1.DERInteger({
                        bigint: this.d
                    }), new pe.asn1.DERInteger({
                        bigint: this.p
                    }), new pe.asn1.DERInteger({
                        bigint: this.q
                    }), new pe.asn1.DERInteger({
                        bigint: this.dmp1
                    }), new pe.asn1.DERInteger({
                        bigint: this.dmq1
                    }), new pe.asn1.DERInteger({
                        bigint: this.coeff
                    })]
                }
                  , t = new pe.asn1.DERSequence(e);
                return t.getEncodedHex()
            }
            ,
            t.prototype.getPrivateBaseKeyB64 = function() {
                return p(this.getPrivateBaseKey())
            }
            ,
            t.prototype.getPublicBaseKey = function() {
                var e = new pe.asn1.DERSequence({
                    array: [new pe.asn1.DERObjectIdentifier({
                        oid: "1.2.840.113549.1.1.1"
                    }), new pe.asn1.DERNull]
                })
                  , t = new pe.asn1.DERSequence({
                    array: [new pe.asn1.DERInteger({
                        bigint: this.n
                    }), new pe.asn1.DERInteger({
                        int: this.e
                    })]
                })
                  , n = new pe.asn1.DERBitString({
                    hex: "00" + t.getEncodedHex()
                })
                  , r = new pe.asn1.DERSequence({
                    array: [e, n]
                });
                return r.getEncodedHex()
            }
            ,
            t.prototype.getPublicBaseKeyB64 = function() {
                return p(this.getPublicBaseKey())
            }
            ,
            t.wordwrap = function(e, t) {
                if (t = t || 64,
                !e)
                    return e;
                var n = "(.{1," + t + "})( +|$\n?)|(.{1," + t + "})";
                return e.match(RegExp(n, "g")).join("\n")
            }
            ,
            t.prototype.getPrivateKey = function() {
                var e = "-----BEGIN RSA PRIVATE KEY-----\n";
                return e += t.wordwrap(this.getPrivateBaseKeyB64()) + "\n",
                e += "-----END RSA PRIVATE KEY-----",
                e
            }
            ,
            t.prototype.getPublicKey = function() {
                var e = "-----BEGIN PUBLIC KEY-----\n";
                return e += t.wordwrap(this.getPublicBaseKeyB64()) + "\n",
                e += "-----END PUBLIC KEY-----",
                e
            }
            ,
            t.hasPublicKeyProperty = function(e) {
                return e = e || {},
                e.hasOwnProperty("n") && e.hasOwnProperty("e")
            }
            ,
            t.hasPrivateKeyProperty = function(e) {
                return e = e || {},
                e.hasOwnProperty("n") && e.hasOwnProperty("e") && e.hasOwnProperty("d") && e.hasOwnProperty("p") && e.hasOwnProperty("q") && e.hasOwnProperty("dmp1") && e.hasOwnProperty("dmq1") && e.hasOwnProperty("coeff")
            }
            ,
            t.prototype.parsePropertiesFrom = function(e) {
                this.n = e.n,
                this.e = e.e,
                e.hasOwnProperty("d") && (this.d = e.d,
                this.p = e.p,
                this.q = e.q,
                this.dmp1 = e.dmp1,
                this.dmq1 = e.dmq1,
                this.coeff = e.coeff)
            }
            ,
            t
        }(),
    // be = n("a524"),

    ge=function () {
        // var e='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB'

        function e(e) {
            void 0 === e && (e = {}),
                e = e || {},
                this.default_key_size = e.default_key_size ? parseInt(e.default_key_size, 10) : 1024,
                this.default_public_exponent = e.default_public_exponent || "010001",
                this.log = e.log || !1,
                this.key = null
        }

        return e.prototype.setKey = function (e) {
            this.log && this.key && console.warn("A key was already set, overriding existing."),
                this.key = new ve(e)
        }
            ,
            e.prototype.setPrivateKey = function (e) {
                this.setKey(e)
            }
            ,
            e.prototype.setPublicKey = function (e) {
                this.setKey(e)
            }
            ,
            e.prototype.decrypt = function (e) {
                try {
                    return this.getKey().decrypt(m(e))
                } catch (t) {
                    return !1
                }
            }
            ,
            e.prototype.encrypt = function (e) {
                try {
                    return p(this.getKey().encrypt(e))
                } catch (t) {
                    return !1
                }
            }
            ,
            e.prototype.sign = function (e, t, n) {
                try {
                    return p(this.getKey().sign(e, t, n))
                } catch (r) {
                    return !1
                }
            }
            ,
            e.prototype.verify = function (e, t, n) {
                try {
                    return this.getKey().verify(e, m(t), n)
                } catch (r) {
                    return !1
                }
            }
            ,
            e.getKey = function (e) {
                if (!this.key) {
                    if (this.key = new ve,
                    e && "[object Function]" === {}.toString.call(e))
                        return void this.key.generateAsync(this.default_key_size, this.default_public_exponent, e);
                    this.key.generate(this.default_key_size, this.default_public_exponent)
                }
                return this.key
            }
            ,
            e.prototype.getPrivateKey = function () {
                return this.getKey().getPrivateKey()
            }
            ,
            e.prototype.getPrivateKeyB64 = function () {
                return this.getKey().getPrivateBaseKeyB64()
            }
            ,
            e.prototype.getPublicKey = function () {
                return this.getKey().getPublicKey()
            }
            ,
            e.prototype.getPublicKeyB64 = function () {
                return this.getKey().getPublicBaseKeyB64()
            }
            ,
            // e.version = be.version,
            e

    }();

function sss(A) {
    var e = t["a"].getKey(), t = (e.n.bitLength() + 7 >> 3) - 11;
    try {
        var n = "", r = "";
        if (A.length > t) return n = A.match(/.{1,50}/g),
            n.forEach((function(A) {var t = e.encrypt(A);
                r += t
            }
            )),
            w(r);
        var a = e.encrypt(A)
          , i = w(a);
        return i
    } catch (s) {
        return s
    }
}

// console.log(.setPublicKey('MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB'))
// console.log(sss('{"inviteMethod":"","businessClassfication":"","mc":"","lx":"ZBGG","dwmc":"","pageIndex":5,"sign":"92b6f0c0fffadd8f7f460e07640d89a8","timestamp":"1690340508158"}'))
// console.log(O.decode(g.unarmor('MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB')))
console.log(ve(ce.e).t('MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB'))
// console.log(O.decode(g.unarmor('MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB')))
// console.log(g.unarmor('MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB'))
// '"{"inviteMethod":"01","businessClassfication":"","mc":"","lx":"ZBGG","dwmc":"","pageIndex":3,"sign":"3b894fcc21c925c4797c6571193f148f","timeStamp":1690265306928}"'
