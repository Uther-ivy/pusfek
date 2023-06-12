# -*- coding: utf-8 -*-
import base64
import re
from html import unescape


import execjs

from binascii import a2b_hex

from Crypto.Cipher import DES, AES
from lxml.builder import unicode




def webjiema(cipher_text):
    null = ""
    true = ""
    false=""
    key = 'jo8j9wGw%6HbxfFn'.encode('utf-8')
    iv = "0123456789ABCDEF".encode('utf-8')
    # key = 'jtkpwangluocom12'.encode('utf-8')
    # iv = "1234567890123456".encode('utf-8')
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    print(base64.b64decode(cipher_text))
    print(a2b_hex(cipher_text))
    plain_text_ = cryptos.decrypt(a2b_hex(cipher_text))
    print(plain_text_)
    Plain_text=bytes.decode(plain_text_)#.replace('',"").replace('',"").replace('',"").replace('',"").replace('',"").replace('',"")
    Plain_text=re.findall(r'(.*})',Plain_text)[0]#.replace('',"").replace('',"").replace('',"").replace('',"").replace('',"").replace('',"")

    print(type(Plain_text),Plain_text)
    Plain_text=eval(Plain_text)
    print(type(Plain_text),Plain_text)
    return Plain_text

def shoujijiemi(data):
    js_infos = '''function deCrypt(t) {
                Object.defineProperty(exports, "__esModule", {
                value: !0
            }), exports.deCrypt = exports.enCrypt = void 0;
                var e = require("./js/38B128C16AECE6CF5ED740C61D4FAC62.js"), r = e.enc.Hex.parse("cd3b2e6d63473cadda38a9106b6b4e07");
                console.log(r)
                var p = e.AES.decrypt(t, r, {
                    mode: e.mode.ECB,
                    padding: e.pad.Pkcs7,
                });
                utf8String = e.enc.Utf8.stringify(p);
                return utf8String;
            }

            module.exports.init = function (arg1) {
                //调用函数，并返回
                console.log(deCrypt(arg1));
            };'''

    dedata = execjs.compile(js_infos).call('deCrypt', data)
    # 读取结果
    print(dedata)
    return dedata


def jiemi_CEB(data):
    null = ""
    true = ""
    false = ""
    # key='829514106, 1081570168, 862257152'.encode()
    # print( key[:8])
    # iv = "0123456789ABCDEF".encode('utf-8')
    # print(a2b_hex(key))
    # key = 'jtkpwangluocom12'.encode('utf-8')
    # iv = "1234567890123456".encode('utf-8')

    # print(a2b_hex(key))
    key = '1qaz@wsx3e'
    cryptos = DES.new((key[:8].encode()),DES.MODE_ECB)
    dedata=base64.b64decode(data)
    plain_text_ = cryptos.decrypt(dedata)

    print(plain_text_)
    Plain_text = bytes.decode(plain_text_)  # .replace('',"").replace('',"").replace('',"").replace('',"").replace('',"").replace('',"")
    Plain_text = re.findall(r'(.*})', Plain_text)[0]  # .replace('',"").replace('',"").replace('',"").replace('',"").replace('',"").replace('',"")

    print(type(Plain_text), Plain_text)
    Plain_text = eval(Plain_text)
    print(type(Plain_text), Plain_text)

#小程序
if __name__ == '__main__':
    # xcx='a4kFevKolhuDJYhfW3f2qyfUJhYt8KEsJEjRQWUYLLAcGSDKl57QHUkjmDDIs/USbIEm8Nid5UTQ9yCFMEGlmoZhZ/5vv/Ir0OPb65sXXk17PtzTIkRaDdi0J9ueRx/WwkANYvKguUnA++bRjzqsZ7HycAUFv75VR1GJqA/AH76oXBIOfPjY6MkGixEReD0NLO30o7mU0tD7xFTk3BDrnxrSQqfICTp5mh9W8hZ8W497PtzTIkRaDdi0J9ueRx/W+/EV8QfZC0pg6lFf7wHcfuQRLsugWGJtAmDWRA7/IaP7ybftsjK/MRw5d8GErNDZEsgwUK9TRNY50v3oP+dAlDWCR3NtO8cgVdRODboD4y+RjX1FPjjvHkjI0HyARy81sfJwBQW/vlVHUYmoD8AfvpB9OI13vcBN0HpezKIVq/2KN0jDOsCfCKahs0LOjk1qIQvlsnajBGx5A6ZIMvlGdUq128IQnwb/Z6R87hJNBRKhGqsXCw90N3X8Y22HxweBzLsy0nYYGAO0oW37a2kFNkaB3BryLSVLdVJQ0q4nkfMdC2/eR+b/oa8Eaby81FtFB3ZBGHJ6vLUogFJN2pimCCr9hogg32AI0KnFKjzZHIawaHDO5kHlqm4cM8qZ+q4J+ayZosH3F91INFzk4jdmIbJJtA/8mpIAnGwIIY74AftLoNdea4gAs7t2ds56fdDIUvVexpRYzKpf2K8wBf9mvKC7L8B47aMlO5QCdGzl5nlPP6935sOQTB7F77RSBl5liwtHR5pcXlsEYLC60LgSoRPMmtACTuWwU5JqCwKOstX7vi/5xEiwjWXOikkmOMgoFXLxhnf3ccr02xkeNBBwDIF8pjXQyPyk5lMC7cYsYvc9H6orNKGla2/dYl12MMmL7juNtJmCXxaQOCDd6T9beOyWZKU1/jxuhoAE6Nv9E6MQjfEU8yakmmBFmbWKKH0kXO/4cKxPbfa2eRAeZuGMtMyJEX8Y66iAGf6YYqimNs4N84VVnUskeQWN0qF4ncI60yr2vB6Lw1I9Cr7+hYvvtDaM5Ru12i0SJWDre+zTbcItsSUYhv3Fk1p4KwAW0Eth0KH0Jn4bG/tbwcpUMRteifBgBWSpmSecL/T3EF6zvos='
    # xcx='8lr7FkeuVfbi9O6o+zpsL8u6lbf5ts2/7fHfQ0zsy1L0kpZLKDbyi+Hsdd+avFFpewj67n7AysjdUqEEYaQU0mOLVpCU9OFDkVE367CKNLFkuHgcR4a86XG0s1MdBioA0Kr4ZrC9z6MZiemkLJRyqKnGpoMAxH/pfJIutLt7chJYdGlUaXB/52SZ9FNXEgnc2EfUBvIk/rGP8KZrfVY5eJgI0PrGXOCgofDOGTRXi8/PohnztMWYK7fOToPDNrRkAdNfMcYfyJ4EdtJ8+bbh9PWekTPHCndDbq+Kp0ykaH+OZTISXpBScXOjsrsGbpsUhbg8w45w5Gtms/l/Uq3rhKzu4D8E+5hOfvxV2rV9xQ5Xx2OAzLi06kPO8n7UJFT9ZUsF0RFRbDD2jTAzJwIyVg=='
    # shoujijiemi(xcx)

#网页
    a = '95780ba0943730051dccb5fe3918f9fe15642a943ae0c649ec8701a8a078dcdf873f8789ca8d21d353a78c2001f2d727fdecc71b938b6ecd3ee104d12aba1e0a37034e55c3d55f51597ac9e039abc37351813f87357f4f617f2135f89db8a21892051502c85ca1a3e80fca7dff62bcfb0f45d309e997bd5b72cdb8874e098d5b30c1ab0521741e9fcac1411080a73a7610d273d8d54461f8dee92593f0e46d2de007eb6e5d38658f662421cc86e237c790ec5b2f48bfc515150c4d5b9a8921a5a37349a5b7bd9ae73ee73f47c0e57706cf4dafe66717560e4566308c9e07cbd23c5ffacbc78817f0e8c6434687a386839394bf774658494c487d3dff972379ad7215b0be030fd91aaf471b56a2362bf73a9883de7a3f75b86d27fb40a30431909cdb4db3b8eab1fe1f184ad8c866fc504d88542cd095e2d8dad19d85d4e4386687a173ac85f8c91f22b73ba0d22c04648baaf5abc540325f44b7b6ba3061411745a273d019cea091db21c490a11898b2955509a70a0963eb0dbf0045ff227c3a773529810c104f23efacce57b414d3070af6ed4c00cc506c4b37711fde2f3718150ee8d964ead2a227c4becc55ef0f3200d34a91a8556a4842880af5c7f251207cd9d5070dde4d377db4e29658bf10f39347e7a2ae2b2fdd46732c35eaf7e9f42b254743c6dddecb12db1b81855717a7e8143d49c6e6fbd2ba8dfa272447eed9281b10eafd67d0d2746591510b58ec505c4b45b481ed2a3237ded5d1d16256cbff4a230625b8b33c7d49232ecefad31735ea61792430f41c1b40a7db1c7522769a52bf41a7043d72edfc08abf0bba843a890e43952ba0e41bc78409da5f5e76189a1f2f4415fa53219fedb5b7e6fb83c34fd28793618418b4abae74d79a5e5bf687d847ff5eb5286823736794bc08ba443291f329cdbe266a718690059492aee2770ab90e09d6402ed145b1517c515b645a64524c6f9dbc71767aeaeedd20134491f21a0a2d8a21a3ec9fd7cf727b1ddbb1c9de5ec7a699344f4a230dc3953211bcc0d56c89b94ad40f308e692275a7f4c0245e527eb711f7596ebe8186811d4db477b6eb241bdfba93f3b2fd9b8794b6eb7a07fcd528b21618ead33db4752207198428570fd16f2eaeb1528eb3b3d006072a9abdce0339913287de75ef29aeba4a76d45789b9f4fbd57d687fea7ae248dc2140d067cbe040ee953b55dea7e373a54b4c6ff209730b7c2cdb3e20da2460218922d134862faedae99e0d28ab63a721aaf6e23bac1eb0f865d726b55645c59da9aaea7fcb64c8548752a3ba64f7a641851347a64b8ab0c72f6c3807cce6768db1c023b967a3c7b59981254f15b2465214b690815dcae114ae259fcb7649ee563f5c955fa5bd4c65d29aa9d92cde7850dcdfc2f02ff0f86a87ad8d4ced73919dd1ca348ac7e5194bb1f3c2e371bce'
    webjiema(a)
    # jiemi_CEB(a)

