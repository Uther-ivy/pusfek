# -*- coding: utf-8 -*-
import base64
import re
from html import unescape

import Crypto
import execjs
from Crypto.Cipher import AES, DES
from binascii import a2b_hex

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
    # return Plain_text

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
    a = '95780ba0943730051dccb5fe3918f9fe15642a943ae0c649ec8701a8a078dcdf6699cdce2eeed5ab4d50ce8bb9545e47b9feb6d9143db00c1eb326915dbb36df44f277cfee4036a728aee8527dfda4e495208c1013354889e78ab1b2e28b58d93d875bb0c568ae2cb9804b70971276693ac2427f633497e036de6d80f29eaefad400706ff98b34d630fbd2026b317922a7ad4c894a187b595dd1a546d81bbd9752321797701039d1afaa2d2e36367ba3f2d1b2cb7bf6126b3b1789e8a80183084f306486dc8fa02cf46de64144151fba70491f1e4d91918c432885a1b1fc9e5838a4c029c64517a3e04feb28c2abc56ab1a3325b113b9c94c1d7cd7dab201478cf2496dfbc0fd1d9bb95624aaa3e08e35ebc60fc8879efb7e4013f135e6f11c0680f16600537c98deca7ea84d572e02b0ee1e9b7c4025e1355f0e371aa39e646d00c473af4e12ae46204884ee5179269a038f150bb88139b260645c67fa00ce609103ca79469bfa967d6281a18bd02956af4265c28293b31db12cc898a45d9839957879648e6cd8a7db229c41efc14c4c2aed62c56652e66c3f7478cdfb9d92ce016b791a72fc00a1c5b2506a0e94cd6b42e0199ba736a5b899bdb4d52ae40ceac4a86eaa83339465685e95d0a7591372c5669a90e3e114e953b224b1ff9ef26dc72cb82584fcdccad3cb7e5fd4bdafcb7752ce268ca80830558b12d9d10042fe00b11103556a3bfdd5a2f49ae59a8c92f8b7be3c777131513b134b1eba9660a96f1f4f82a77b31ae3d93ee630b11fe03c46e95de7d22b814d6794d505708b746f2efec444849c473aef613089d25acdbd7a48258065e8600ca4f72095008229004999c78f74eb52ce75b007b5454aa4b39edf60f472adbbce3db5dd6bab74be40f7af7e9d39e40688b2bc975e7fcb1399f6b66369b5fd81b2d2413842175bd122d4af031ebe47b01d208a7677b1ac1fb51da5e9e2cb005aee15fcaa27dc7d5688fc09beaba10865e3d18ceb5c0d5dd77bdef83dd47085fc8e53a0f84b5b416a2add039b89a3885bc39487f2c29e2f944e1efa9c3bde2d27e828e5e4287ccf346d98bd7682dc9fe0bb5164bc51662e7f84a7df5b9442ad93a27456c90de4836e6ad28d0fb83eaafc5296bc71d3ec9d5a3663374a2b4cf6645ef84fb7755e01c78742d4c03c8ed4b0c49dad8bec8116c99c74028f94fadec74a60a1aa7fa21ef98042d79d26332a5f49f170226346fe868d34ed4faa6bcee0df57600c3867a0ca7b5273faa58f729b8ec422a14abc76c23a9443e14bec7d9563ad4615823a53fd64f0a53e541b0e58a217538d6f60e292c2f05b85fd47fb5dbc01fb901c609797a99188b46da2e03f491bf8aa7eb0da0f9b026f799d32a57af34a7582cd4be572db324f1e83ec5b4e611f48fe662a2fc9ce5880a4dffdf0a1d478cab546e2e6ad2f8a675b3f59c6f37f3b905a0d9c1daff68c88c3f52b5062ae8ea297685cfebeaaae87ce0e443aae876df2493a5b0ba5c231f3088c4dcc6d3a6d32213569176825f5ede61a3b0b940f742c6216b6ac58453a1599cdf97d59c05a9195c1f4c912946920b2945fca65b5d23a904d6694a89363b950e7a175643dace4e5bd7f92c7cde33bdd55cbdefee413a0cd85326312b11bf57e73cc6395a5fec5c3f328058849d6c1fcdf6fba9215dbe17d4d869760567b277bb101d714544b4d1ebf610d8c04ceb5036add93b22b9888ed794f5082286e3eb5d369d74d04676587e26b32180486c2da9b95df947163e3d4896086c96fba23d66b248841c41c77c1a6edf4bcb272ab8d3ddc1a4ddb049f5a650f77d786bd771ae719b35b315e20bd543ac5bee1f5d0742965e2c08d329266c7eb2dc217cce60f040c0eca1f654bdf4c5fd1c1394abd4296d003645db07207bd88e8a9273119c9a1ffe90f8ccd5e8baddc917ec09bd505fcc760f8b0b88448ad4ff1cc23770c829530b4f2abea6c395bb95a66caa21fc131fe2cf9719a6fc3f38f506982eba30d5f3b03321278c1385936808611a21ffa6762f7b3c6aa0353d30cbf1ffdc5fa8cf112f7cdf2d4793d72dd0820b692620bca9066827e17776b07fdbd0270fe3eeeb70217ed73b536a19db4cc4af9bf641413d676b0e4bc799e007c1687924224eb3276958198311f1cc41bf0cbf71ec5eb180926ef3e887d3ea12fe6ff6ba6ef4a5b2af56e26ea49cb98d1a29becbc6bb71edca990aaf983c3fd878123d4d936c62171380880b9ea899f55938a9ee00b8982f927bee850a7a4794b6acfbd6cee916301bde4e1ae4602381130e8cc31745080ccbef87d5a5051f6006a7bb4400b0867a0f9770de7b87800fe67ec89eef7ea9488e1ff656ae21f8d60ff71e3bb34169d1f3f7fcc7f5d6d4c9054d5ae24b9b34c0aeb9e3772e81c78124e6bb9845fb8baf06a2d28cf41a22ff04a2aa110ff9519bb3e585b9c9bc3a8179baf43cc8c030c00b815dec5392a7674c6d96f45baea5be3f924d42b47860dc78b1770c50a9dba6e0cb0ddfb71107547e8800137e3de9431d47b0f65098beb3be21d01f165dc956276f28ac8ec7ef89e4f06798ba0890288759f4def3e6350582eee8271e63ed377df59b8c71e5929dd04443c7884c9bf9f0adc9c2da3d616a3b4a33c96478e235632523b89c7bc0ba1e86a6eff8a016e5aaeba35f49a82408b7c801a622a0ea9966a8866906f389bdcb6e38db04e8cd641dda35c29c3c356c6c4b3f7e9e244497e9588aaa933296668842ba92c2b0ce2221bff72c6860171440acb83d88560d7c575ab270270b2edfdb2ee628192f0b96604047e42378accc7410057736f692aba3fafa1da0288ca73c2d45ba96bdb0cdc8507db8f72b7dc63e2f1f30712c2167f414c442a3ef3d4a00b702dc67654cf0c93b1631113e956d944fa9d6723223c69fa3d32aa267c80cadf1da9c155702439fdb1744008d6084a736a882efdf7dfae112ff2c7457818b57806d12881929aa747bf872e48eb1a42809c561ceab867bf6c0afbe47c7754c9724e9dae6d7a26c2fc26dc36891c47d80f7cb6d456a36e8a5833a7148c419c562d67ebdfc1950462b0a2ee37530f0ed686d41982597a20ca5c9b680fe9eb7077adbdc0e711a5280f653c6606380abfad72b7756801369fa6e968fdb45622e57e3e34f38f8524d649539ed145be8fb079929661969eae8440d07604015aca8c2fd559308b799ab2affd529d2108eb15cddb27'
    webjiema(a)
    # jiemi_CEB(a)

