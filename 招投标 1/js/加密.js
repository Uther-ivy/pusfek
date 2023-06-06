const CryptoJS=require('crypto-js')
const {JSDOM} =require('jsdom');
const {ASN1} =require('asn1');
const {prototype}=require('prototype')
const jsdom =new JSDOM('<!dictype html><html><body></body></html>');
const {window}=jsdom;
global.window=window;
global.asn1=ASN1;
global.prototype=prototype
global.document=window.document;
global.navigator={
    userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
};
const {JSEncrypt}=require('../js/jsencrypt.min.js')
function randomString(len) {
    len = len || 32;
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
    var maxPos = $chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}
function Encrypt(word, randomKey) {
    key = CryptoJS.enc.Utf8.parse(randomKey);
    var srcs = CryptoJS.enc.Utf8.parse(word);
    var encrypted = CryptoJS.AES.encrypt(srcs, key, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString()
}
function encry(userData,){
    var randomStr = randomString(16);
    var requestData = Encrypt(JSON.stringify(userData),randomStr);
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfXfMzgg4m5RRLg2vcrYBFN4sBhE1VtW1sBkXxC5wtCRaOZv0kudk9CIQfU6c+eEaaZKUnygxHWdSqdwURCE0IKgLcolXF+RHmu/rl977FfjRg9pAkBg5z05PfHDqWqkIsqX0iRaSP31BUZOgtwafbiBv2dBvRBMdq03ty4q8OQQIDAQAB\n");
    var encrypted = encrypt.encrypt(randomStr);
    var data={
        'requestData':requestData,
        'encrypted':encrypted
    }
    return data
}
function Encrypts(encrypted) {
    var privateKey = "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAITfvlC8+Nr+vz3DnhuCWW41ax8PG+rCiXt/f4XjRMlj9ZC2AuMMbtHLsTMLhCrhgHt1MxdcoYtqvQfxu4AVOh6pZrxMr2AiyNpw8SecmM3m0YWYNc7tnUB6/vlLyQduikD4qaxNiB5FcUiRpiRoLpz7rT6UV+/zDh+ibgvZRLDRAgMBAAECgYB7/mMV6tJ7YkBKPdK8Lw6PZq/5Att1XmZ3ZYo2Adg96tbMXN0izYZYprFMRhHnBhokm0C7K0jg1hFiaXUkWCqr83H+Y+DZ7js9NDhApPYAELQDIu288/nz34mjU/wnIGWP6WK5PCd1QjR8ltFay1TDLecdavHHjWGfHOMYnY5/dQJBAOZ4ICB+VrXMwR8KUR3r420YAHPwQDQKDetMHwgYHtFUH/k3CtKzPrltx103OhQcKyfrkoPj8SREZZISaBEQL6cCQQCTl+pjOSMud4hFTvfTnkGx9EZT3dBAv31ZfzHCu4g41FxRLyJLY6iKce069IhMjC2gfoLtwDLM/dKzRAuw9+rHAkAd9/zlfMg1t7xdFvBZXbUjGH3mlZUjrzMEJ8/ZM5m+SpwlwfyMTXaYkifcfTP2LXuHI2DX+an/t00l43LY1Sv9AkAEgQ5WGNhKArvV4aMOgjXfCGVdCdfhIfbhVFBgcPinQ1PN5nJVeqUaFH/43J2MOHrr+vBj8Qmb1+MmNV1l+SrhAkArJjCosjMI32RT3GmC6+gwxADR9Ib53yDHwRoMeO34dgK3hj3+e66Jhpcht3AjXBVs7bF9xzXcePpxxCka9cEv";
    var decrypt = new JSEncrypt();
    decrypt.setPrivateKey(privateKey);
    return decrypt.decrypt(encrypted);
}
function Decrypt(word, randomKey) {
    key = CryptoJS.enc.Utf8.parse(randomKey);
    var decrypt = CryptoJS.AES.decrypt(word, key, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return CryptoJS.enc.Utf8.stringify(decrypt).toString()
}
function decrys(requestData,encrypted){
    var aesKey= Encrypts(encrypted)
    var dataStr = Decrypt(requestData,aesKey).replace(/\r\n/g,"").replace(/\\/g,"");
    var data = JSON.parse(dataStr);
    return data
}