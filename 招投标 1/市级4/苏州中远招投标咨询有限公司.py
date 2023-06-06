# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
import datetime
from save_database import process_item

# 苏州中远招投标咨询有限公司
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.szzyztb.com/ShowASP/News/News.aspx?c_id=3', #工程招标
           ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data = {
                '__VIEWSTATE': '/wEPDwUKLTQxMzkwODk1MQ9kFgQCAQ9kFgZmDxYCHgRocmVmBRsuLi9Ta2lucy9pbXByZXp6L2dsb2JhbC5jc3NkAgEPFgIfAAUbLi4vU2tpbnMvaW1wcmV6ei9tb2R1bGUuY3NzZAICDxYCHwAFGy4uL1NraW5zL2ltcHJlenovaW5zaWRlLmNzc2QCAw9kFggCCg9kFgICBQ8WAh4JaW5uZXJodG1sBeEfPGRpdiBjbGFzcz0iZ3JhYm94IHNpZGVDb2wiPiAgICAgPGgzPiA8YSBocmVmPScnPjxzcGFuIGlkPSJjb2xuYW1lMTAiPuWGhemhteagt+W8jzwvc3Bhbj48L2E+PC9oMz4gICAgICAgICA8ZGl2IGNsYXNzPSJpbmRleF9ncmFwaGljIGluZGV4Q29uIiBydW5hdD0ic2VydmVyIj4gICAgICAgICA8ZGwgY2xhc3M9ImNsZWFyZml4Ij48ZGl2PjxwPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+DQojQ29udGFpbmVye3dpZHRoOjEwMCV9DQojQ29udGFpbmVyICNIZWFkZXJ7d2lkdGg6MTAwJX0NCiNkaXZIZWFke3dpZHRoOjEwMDBweDttYXJnaW46MHB4IGF1dG87fQ0KI2xvZ297d2lkdGg6MTAwMHB4O21hcmdpbjowcHggYXV0bzt9DQpib2R5e2JhY2tncm91bmQ6dXJsKC9VcGxvYWQvc3p6eXp0YmNvbTE1MTEyNy9GQ0tFZGl0b3IvaW1hZ2UvQkouanBnKSB0b3AgbGVmdCByZXBlYXQteDsgYmFja2dyb3VuZC1jb2xvcjojZmZmO2ZvbnQtZmFtaWx5OiLlvq7ova/pm4Xpu5EifQ0KLmluZGV4Q29uIHtwYWRkaW5nOjFweCAycHg7fQ0KI3RvcGxpbmsgbGkge2JhY2tncm91bmQ6bm9uZX0NCi5tZW51e2JhY2tncm91bmQ6bm9uZTtwYWRkaW5nLWJvdHRvbTo1cHg7fQ0KLm1lbnUgLnBvc2l0aW9ue2xlZnQ6MTBweDt9DQoubWVudXNlbCBhOmxpbmt7Y29sb3I6I2ZmZn0NCi5tZW51c2VsIGE6dmlzaXRlZHtjb2xvcjojZmZmfQ0KLm1lbnVzZWwgYTpob3Zlcntjb2xvcjojZmZkMjAwfQ0KLm1lbnVzZWwgYTpob3ZlciB7YmFja2dyb3VuZDpub25lfQ0KLnBvc2l0aW9uIHVsIHtiYWNrZ3JvdW5kLWNvbG9yOiMwMDg3Y2I7Ym9yZGVyOjBweDtmb250LXNpemU6MTJweH0NCi5pbmRleF9waWMgdWwgbGkgZGl2LmltZyB7Ym9yZGVyOiAycHggc29saWQgI2JjYmNiYztiYWNrZ3JvdW5kLWNvbG9yOiAjYmNiY2JjO30NCiNGb290ZXIge2JhY2tncm91bmQ6IHVybCgvVXBsb2FkL3N6enl6dGJjb20xNTExMjcvRkNLRWRpdG9yL2ltYWdlL2YxMS5qcGcpIHRvcCByZXBlYXQ7fQ0KI0Zvb3RlciB7Y29sb3I6ICNmZmY7fQ0KI0Zvb3RlciBhOmxpbmt7Y29sb3I6I2ZmZn0NCiNGb290ZXIgYTp2aXNpdGVke2NvbG9yOiNmZmZ9DQojRm9vdGVyIGE6aG92ZXJ7Y29sb3I6I2ZmZDIwMH0NCi5pbmRleENvbntwYWRkaW5nOjBweH0NCiNzaWRlMXtkaXNwbGF5Om5vbmV9DQouaW5kZXhfbGlzdCAudWxpc3QgZGwgZGQgc3Bhbi5wdWJ0aW1le2Rpc3BsYXk6bm9uZX0NCi5zaWRlQ29sIC5pbmRleENvbiBhOmxpbmt7Y29sb3I6IzAwMDAwMH0gLnNpZGVDb2wgLmluZGV4Q29uIGE6dmlzaXRlZHtjb2xvcjojMDAwMDAwfSAuc2lkZUNvbCAuaW5kZXhDb24gYTpob3Zlcntjb2xvcjojZmZmfSAubWFpbkNvbiB7cGFkZGluZzogMHB4IDBweCAwcHg7fSAuc2lkZUNvbCAuaW5kZXhDb24sIC5zaWRlQ29sIC5pbmRleF9zbGlkZSB7IG1hcmdpbjogMCAwcHggMDsgYm9yZGVyLWxlZnQ6IDBweCBzb2xpZCAjZmZmOyBib3JkZXItcmlnaHQ6IDBweCBzb2xpZCAjZmZmOyBiYWNrZ3JvdW5kLWNvbG9yOiAjZmZmOyBjb2xvcjogIzkwOTY5ODt9DQojVGJvZHkge2JhY2tncm91bmQ6dXJsKC9VcGxvYWQvNTg4NTE4NmNuMTQxMDEwL0ZDS0VkaXRvci9iYWkuanBnKSBsZWZ0IHJlcGVhdC15OykgdG9wIGxlZnQgbm8tcmVwZWF0fSANCi5tYWluLXRpdGxlIHtiYWNrZ3JvdW5kOnVybCgvVXBsb2FkL3N6enl6dGJjb20xNTExMjcvRkNLRWRpdG9yL2ltYWdlL2EuanBnKSB0b3AgbGVmdCBuby1yZXBlYXQ7Ym9yZGVyOiAxcHggc29saWQgI2U4ZThlODtwYWRkaW5nLWxlZnQ6MzJweH0gDQouc2lkZUNvbCBoMyBzcGFue2JhY2tncm91bmQ6dXJsKC9VcGxvYWQvc3p6eXp0YmNvbTE1MTEyNy9GQ0tFZGl0b3IvaW1hZ2UvbnkxLmpwZykgbGVmdCB0b3Agbm8tcmVwZWF0O3BhZGRpbmctbGVmdDoyNHB4O2xpbmUtaGVpZ2h0OjQwcHg7Y29sb3I6IzAwMDAwMH0gDQouc2lkZUNvbCBoMyB7YmFja2dyb3VuZDpub25lfSAuZ3JhYm94IHtiYWNrZ3JvdW5kOiBub25lO30gDQouc2lkZUNvbCBoMyB7aGVpZ2h0OjM2cHg7fQ0KLm1haW5Db24gZGwgZHQgew0KYmFja2dyb3VuZDogdXJsKC9VcGxvYWQvc3p6eXp0YmNvbTE1MTEyNy9GQ0tFZGl0b3IvaW1hZ2UvQkIucG5nKSBsZWZ0IGNlbnRlciBuby1yZXBlYXQ7fQ0KDQo8L3N0eWxlPjwvcD48c2NyaXB0Pg0Kd2luZG93Lm9ubG9hZD1mdW5jdGlvbigpew0KdmFyIG49ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInNpZGUyIikuZ2V0RWxlbWVudHNCeVRhZ05hbWUoImRpdiIpOw0Kbi5pdGVtKDEpLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7DQp9DQo8L3NjcmlwdD48ZGl2PiAgICAgICAgIDwvZGw+ICAgICA8L2Rpdj48L2Rpdj48ZGl2IGNsYXNzPSJncmFib3ggc2lkZUNvbCI+ICAgICA8aDM+IDxhIGhyZWY9Jyc+PHNwYW4gaWQ9ImNvbG5hbWUxMSI+5qCP55uu5a+86IiqPC9zcGFuPjwvYT48L2gzPiAgICAgICAgIDxkaXYgY2xhc3M9ImluZGV4X2dyYXBoaWMgaW5kZXhDb24iIHJ1bmF0PSJzZXJ2ZXIiPiAgICAgICAgIDxkbCBjbGFzcz0iY2xlYXJmaXgiPjxkaXY+PHA+PHN0eWxlIHR5cGU9InRleHQvY3NzIj4uZmwxeyBmbG9hdDpsZWZ0OyBmb250LWZhbWlseToi5b6u6L2v6ZuF6buRIjsgZm9udC1zaXplOjE0cHg7IGJhY2tncm91bmQ6dXJsKC9VcGxvYWQvc3p6eXp0YmNvbTE1MTEyNy9GQ0tFZGl0b3IvaW1hZ2UvbDFhLmpwZyk7IHdpZHRoOjIzMHg7IGhlaWdodDozM3B4OyBsaW5lLWhlaWdodDozM3B4OyBsaXN0LXN0eWxlOm5vbmU7IHRleHQtYWxpZ246Y2VudGVyfQ0KLmZsMSBhe2NvbG9yOiNmZmY7IHRleHQtZGVjb3JhdGlvbjpub25lO3dpZHRoOjIzMHB4OyBoZWlnaHQ6MzNweDsgZGlzcGxheTpibG9ja30NCi5mbDEgYTpob3Zlcntjb2xvcjojZmZmOyB0ZXh0LWRlY29yYXRpb246dW5kZXJsaW5lfQ0KLmZsMnsgZmxvYXQ6bGVmdDsgZm9udC1mYW1pbHk6IuW+rui9r+mbhem7kSI7IGZvbnQtc2l6ZToxNHB4OyBiYWNrZ3JvdW5kOnVybCgvVXBsb2FkL3N6enl6dGJjb20xNTExMjcvRkNLRWRpdG9yL2ltYWdlL29uMS5qcGcpOyB3aWR0aDoyMzBweDsgaGVpZ2h0OjMzcHg7IGxpbmUtaGVpZ2h0OjMzcHg7IGxpc3Qtc3R5bGU6bm9uZTsgdGV4dC1hbGlnbjpjZW50ZXI7IG1hcmdpbi10b3A6NXB4fQ0KLmZsMiBhe2NvbG9yOiMzMzMzMzM7IHRleHQtZGVjb3JhdGlvbjpub25lOyB3aWR0aDoyMzBweDsgaGVpZ2h0OjMzcHg7IGRpc3BsYXk6YmxvY2t9DQouZmwyIGE6aG92ZXJ7Y29sb3I6I2ZmZjsgdGV4dC1kZWNvcmF0aW9uOnVuZGVybGluZTsgYmFja2dyb3VuZDp1cmwoL1VwbG9hZC9zenp5enRiY29tMTUxMTI3L0ZDS0VkaXRvci9pbWFnZS9sMWEuanBnKX08L3N0eWxlPjwvcD4NCjxkaXYgc3R5bGU9IndpZHRoOiAyMzBweDsiPg0KPHVsPg0KICAgIDxsaSBjbGFzcz0iZmwxIj48YSBocmVmPSIvaW5kZXguYXNweCI+572R56uZ6aaW6aG1PC9hPjwvbGk+DQogICAgPGxpIGNsYXNzPSJmbDIiPjxhIGhyZWY9Ii9TaG93QVNQL1BpYy9TaW5nbGUuYXNweD9jaWQ9MiZhbXA7Y19pZD0yIj7lhazlj7jnroDku4s8L2E+PC9saT4NCiAgICA8bGkgY2xhc3M9ImZsMiI+PGEgaHJlZj0iL1Nob3dBU1AvTmV3cy9OZXdzLmFzcHg/Y2lkPTMmYW1wO2NfaWQ9MyI+5oub5qCH5L+h5oGvPC9hPjwvbGk+DQogICAgPGxpIGNsYXNzPSJmbDIiPjxhIGhyZWY9Ii9TaG93QVNQL05ld3MvTmV3cy5hc3B4P2NpZD00JmFtcDtjX2lkPTQiPuihpeWFhemAmuefpTwvYT48L2xpPg0KICAgIDxsaSBjbGFzcz0iZmwyIj48YSBocmVmPSIvU2hvd0FTUC9OZXdzL05ld3MuYXNweD9jaWQ9NSZhbXA7Y19pZD01Ij7kuK3moIfkv6Hmga88L2E+PC9saT4NCiAgICA8bGkgY2xhc3M9ImZsMiI+PGEgaHJlZj0iL1Nob3dBU1AvTmV3cy9OZXdzLmFzcHg/Y2lkPTYmYW1wO2NfaWQ9NiI+5rOV5b6L5rOV6KeEPC9hPjwvbGk+DQogICAgPGxpIGNsYXNzPSJmbDIiPjxhIGhyZWY9Ii9TaG93QVNQL1BpYy9TaW5nbGUuYXNweD9jaWQ9OCZhbXA7Y19pZD04Ij7ogZTns7vmiJHku6w8L2E+PC9saT4NCiAgICA8cD4mbmJzcDs8L3A+DQo8L3VsPg0KPC9kaXY+PGRpdj4gICAgICAgICA8L2RsPiAgICAgPC9kaXY+PC9kaXY+ZAILDxYCHwEFDOaLm+agh+S/oeaBr2QCDA8WAh8BBd4wPGRpdiBjbGFzcz0ibmV3c2xpc3QiPjxkbD48ZHQ+PHNwYW4+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MTYiPuiLj+W3nuW4guWQtOS4reWMuuWfjuWNl+ihl+mBk+eip+azouS6jOadkeeJqeS4mueuoS4uLjwvYT48L3NwYW4+PC9kdD48ZGQgY2xhc3M9InByZXZpZXciPuiLj+W3nuS4rei/nOaLm+aKleagh+WSqOivouaciemZkOWFrOWPuOWPl+iLj+W3nuW4guWQtOS4reWMuuWfjuWNl+ihl+mBk+eip+azouS6jOadkeeJqeS4mueuoeeQhuWnlOWRmOS8mueahOWnlOaJmO+8jOWwseWFtumcgOimgeeahOeJqeS4muacjeWKoei/m+ihjOernuS6ieaAp+eji+WVhumHh+i0reOAguasoui/juaciei1hOagvOeahOS+m+W6lOWVhuWJjeadpeWPguWKoOacrOasoeernuS6ieaAp+eji+WVhumHh+i0rea0u+WKqOOAguS4gOOAgemHh+i0remhueebruamguWGte+8mjHjgIHph4fotK3lhoUuLi48L2RkPjxkZCBjbGFzcz0iaW5mbyI+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MTYiPuafpemYheWFqOaWhy4uLjwvYT7kvZzogIXvvJo8c3Bhbj7nrqHnkIblkZg8L3NwYW4+5Y+R6KGo5LqO77yaPHNwYW4+MjAyMy00LTc8L3NwYW4+IOeCueWHu++8mjxzcGFuPjcxPC9zcGFuPjwvZGQ+PC9kbD48ZGw+PGR0PjxzcGFuPjxhIGhyZWY9Ii4uL05ld3MvTmV3SW5mby5hc3B4P2luZm9JZD0xNTEzIj7oi4/lt57luILlkLTkuK3ljLrlpoflubzkv53lgaXmiYDlhbPkuo7kurrkvZPmiJDliIYuLi48L2E+PC9zcGFuPjwvZHQ+PGRkIGNsYXNzPSJwcmV2aWV3Ij4gICAg6IuP5bee5Lit6L+c5oub5oqV5qCH5ZKo6K+i5pyJ6ZmQ5YWs5Y+45Y+X6IuP5bee5biC5ZC05Lit5Yy65aaH5bm85L+d5YGl5omA55qE5aeU5omY77yM5bCx5YW26ZyA6KaB55qE5Lq65L2T5oiQ5YiG5YiG5p6Q5Luq6L+b6KGM56ue5LqJ5oCn56OL5ZWG6YeH6LSt44CC5qyi6L+O5pyJ6LWE5qC855qE5L6b5bqU5ZWG5YmN5p2l5Y+C5Yqg5pys5qyh56ue5LqJ5oCn56OL5ZWG6YeH6LSt5rS75Yqo44CC5LiA44CB6YeH6LSt6aG555uu5qaC5Ya177yaMeOAgemHh+i0reWGheWuue+8muS6ui4uLjwvZGQ+PGRkIGNsYXNzPSJpbmZvIj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUxMyI+5p+l6ZiF5YWo5paHLi4uPC9hPuS9nOiAhe+8mjxzcGFuPueuoeeQhuWRmDwvc3Bhbj7lj5Hooajkuo7vvJo8c3Bhbj4yMDIzLTQtMzwvc3Bhbj4g54K55Ye777yaPHNwYW4+Nzc8L3NwYW4+PC9kZD48L2RsPjxkbD48ZHQ+PHNwYW4+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MTIiPuiLj+W3nuW4guWQtOS4reWMuuWmh+W5vOS/neWBpeaJgOWFs+S6juS4reiAs+WIhuaekC4uLjwvYT48L3NwYW4+PC9kdD48ZGQgY2xhc3M9InByZXZpZXciPiAgIOiLj+W3nuS4rei/nOaLm+aKleagh+WSqOivouaciemZkOWFrOWPuOWPl+iLj+W3nuW4guWQtOS4reWMuuWmh+W5vOS/neWBpeaJgOeahOWnlOaJmO+8jOWwseWFtumcgOimgeeahOS4reiAs+WIhuaekOS7qui/m+ihjOernuS6ieaAp+eji+WVhumHh+i0reOAguasoui/juaciei1hOagvOeahOS+m+W6lOWVhuWJjeadpeWPguWKoOacrOasoeernuS6ieaAp+eji+WVhumHh+i0rea0u+WKqOOAguS4gOOAgemHh+i0remhueebruamguWGte+8mjHjgIHph4fotK3lhoXlrrnvvJrkuK3ogLPliIbmnpAuLi48L2RkPjxkZCBjbGFzcz0iaW5mbyI+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MTIiPuafpemYheWFqOaWhy4uLjwvYT7kvZzogIXvvJo8c3Bhbj7nrqHnkIblkZg8L3NwYW4+5Y+R6KGo5LqO77yaPHNwYW4+MjAyMy00LTM8L3NwYW4+IOeCueWHu++8mjxzcGFuPjc4PC9zcGFuPjwvZGQ+PC9kbD48ZGw+PGR0PjxzcGFuPjxhIGhyZWY9Ii4uL05ld3MvTmV3SW5mby5hc3B4P2luZm9JZD0xNTExIj7oi4/lt57nkZ7popDogIHlubTnl4XljLvpmaLmnInpmZDlhazlj7jlhbPkuo7ljLvnlpcuLi48L2E+PC9zcGFuPjwvZHQ+PGRkIGNsYXNzPSJwcmV2aWV3Ij7oi4/lt57kuK3ov5zmi5vmipXmoIflkqjor6LmnInpmZDlhazlj7jlj5foi4/lt57nkZ7popDogIHlubTnl4XljLvpmaLmnInpmZDlhazlj7jnmoTlp5TmiZjvvIzlsLHlhbbpnIDopoHnmoTljLvnlpforr7lpIfkuIDmibnov5vooYznq57kuonmgKfno4vllYbph4fotK3jgILmrKLov47mnInotYTmoLznmoTkvpvlupTllYbliY3mnaXlj4LliqDmnKzmrKHnq57kuonmgKfno4vllYbph4fotK3mtLvliqjjgILkuIDjgIHph4fotK3pobnnm67mpoLlhrXvvJox44CB6YeH6LSt5YaF5a6577ya5Yy755aX6K6+5aSHLi4uPC9kZD48ZGQgY2xhc3M9ImluZm8iPjxhIGhyZWY9Ii4uL05ld3MvTmV3SW5mby5hc3B4P2luZm9JZD0xNTExIj7mn6XpmIXlhajmlocuLi48L2E+5L2c6ICF77yaPHNwYW4+566h55CG5ZGYPC9zcGFuPuWPkeihqOS6ju+8mjxzcGFuPjIwMjMtMy0yOTwvc3Bhbj4g54K55Ye777yaPHNwYW4+MTA3PC9zcGFuPjwvZGQ+PC9kbD48ZGw+PGR0PjxzcGFuPjxhIGhyZWY9Ii4uL05ld3MvTmV3SW5mby5hc3B4P2luZm9JZD0xNTA1Ij7oi4/lt57luILnq4vljLvpmaLmnKzpg6jlhbPkuo7miYvmnK/lmajmorDkuIDmibnpobkuLi48L2E+PC9zcGFuPjwvZHQ+PGRkIGNsYXNzPSJwcmV2aWV3Ij7oi4/lt57kuK3ov5zmi5vmipXmoIflkqjor6LmnInpmZDlhazlj7jlj5foi4/lt57luILnq4vljLvpmaLmnKzpg6jnmoTlp5TmiZjvvIzlsLHlhbbpnIDopoHnmoTmiYvmnK/lmajmorDkuIDmibnov5vooYznq57kuonmgKfno4vllYbph4fotK3jgILmrKLov47mnInotYTmoLznmoTkvpvlupTllYbliY3mnaXlj4LliqDmnKzmrKHnq57kuonmgKfno4vllYbph4fotK3mtLvliqjjgILkuIDjgIHph4fotK3pobnnm67mpoLlhrXvvJox44CB6YeH6LSt5YaF5a6577ya5omL5pyv5Zmo5qKw5LiA5om5IDLjgIEuLi48L2RkPjxkZCBjbGFzcz0iaW5mbyI+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MDUiPuafpemYheWFqOaWhy4uLjwvYT7kvZzogIXvvJo8c3Bhbj7nrqHnkIblkZg8L3NwYW4+5Y+R6KGo5LqO77yaPHNwYW4+MjAyMy0zLTE3PC9zcGFuPiDngrnlh7vvvJo8c3Bhbj4xNTA8L3NwYW4+PC9kZD48L2RsPjxkbD48ZHQ+PHNwYW4+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MDQiPuiLj+W3nuW4gueri+WMu+mZouacrOmDqOWFs+S6jueUteWKqOaJi+acr+W6iumhueebri4uLjwvYT48L3NwYW4+PC9kdD48ZGQgY2xhc3M9InByZXZpZXciPuiLj+W3nuS4rei/nOaLm+aKleagh+WSqOivouaciemZkOWFrOWPuOWPl+iLj+W3nuW4gueri+WMu+mZouacrOmDqOeahOWnlOaJmO+8jOWwseWFtumcgOimgeeahOeUteWKqOaJi+acr+W6iui/m+ihjOernuS6ieaAp+eji+WVhumHh+i0reOAguasoui/juaciei1hOagvOeahOS+m+W6lOWVhuWJjeadpeWPguWKoOacrOasoeernuS6ieaAp+eji+WVhumHh+i0rea0u+WKqOOAguS4gOOAgemHh+i0remhueebruamguWGte+8mjHjgIHph4fotK3lhoXlrrnvvJrnlLXliqjmiYvmnK/luoogMuOAgemHh+i0rS4uLjwvZGQ+PGRkIGNsYXNzPSJpbmZvIj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwNCI+5p+l6ZiF5YWo5paHLi4uPC9hPuS9nOiAhe+8mjxzcGFuPueuoeeQhuWRmDwvc3Bhbj7lj5Hooajkuo7vvJo8c3Bhbj4yMDIzLTMtMTc8L3NwYW4+IOeCueWHu++8mjxzcGFuPjE0NTwvc3Bhbj48L2RkPjwvZGw+PGRsPjxkdD48c3Bhbj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwMyI+6IuP5bee5biC56uL5Yy76Zmi5pys6YOo5YWz5LqO5a6e6aqM5a6k5aSn5Z6L5Luq5ZmoLi4uPC9hPjwvc3Bhbj48L2R0PjxkZCBjbGFzcz0icHJldmlldyI+6IuP5bee5Lit6L+c5oub5oqV5qCH5ZKo6K+i5pyJ6ZmQ5YWs5Y+45Y+X6IuP5bee5biC56uL5Yy76Zmi5pys6YOo55qE5aeU5omY77yM5bCx5YW26ZyA6KaB55qE5a6e6aqM5a6k5aSn5Z6L5Luq5Zmo566h55CG6L2v5Lu257O757uf6L+b6KGM56ue5LqJ5oCn56OL5ZWG6YeH6LSt44CC5qyi6L+O5pyJ6LWE5qC855qE5L6b5bqU5ZWG5YmN5p2l5Y+C5Yqg5pys5qyh56ue5LqJ5oCn56OL5ZWG6YeH6LSt5rS75Yqo44CC5LiA44CB6YeH6LSt6aG555uu5qaC5Ya177yaMeOAgemHh+i0reWGheWuue+8muWunumqjC4uLjwvZGQ+PGRkIGNsYXNzPSJpbmZvIj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwMyI+5p+l6ZiF5YWo5paHLi4uPC9hPuS9nOiAhe+8mjxzcGFuPueuoeeQhuWRmDwvc3Bhbj7lj5Hooajkuo7vvJo8c3Bhbj4yMDIzLTMtMTY8L3NwYW4+IOeCueWHu++8mjxzcGFuPjE5MTwvc3Bhbj48L2RkPjwvZGw+PGRsPjxkdD48c3Bhbj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwMiI+6IuP5bee5biC56uL5Yy76Zmi5pys6YOo5YWz5LqO5bCB5Y+j5py6562J6K6+5aSH5LiALi4uPC9hPjwvc3Bhbj48L2R0PjxkZCBjbGFzcz0icHJldmlldyI+6IuP5bee5Lit6L+c5oub5oqV5qCH5ZKo6K+i5pyJ6ZmQ5YWs5Y+45Y+X6IuP5bee5biC56uL5Yy76Zmi5pys6YOo55qE5aeU5omY77yM5bCx5YW26ZyA6KaB55qE6ZOF6KGj562J6K6+5aSH5LiA5om56L+b6KGM56ue5LqJ5oCn56OL5ZWG6YeH6LSt44CC5qyi6L+O5pyJ6LWE5qC855qE5L6b5bqU5ZWG5YmN5p2l5Y+C5Yqg5pys5qyh56ue5LqJ5oCn56OL5ZWG6YeH6LSt5rS75Yqo44CC5LiA44CB6YeH6LSt6aG555uu5qaC5Ya177yaMeOAgemHh+i0reWGheWuue+8muWwgeWPo+acuuetieiuvuWkh+S4gOaJuS4uLjwvZGQ+PGRkIGNsYXNzPSJpbmZvIj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwMiI+5p+l6ZiF5YWo5paHLi4uPC9hPuS9nOiAhe+8mjxzcGFuPueuoeeQhuWRmDwvc3Bhbj7lj5Hooajkuo7vvJo8c3Bhbj4yMDIzLTMtMTU8L3NwYW4+IOeCueWHu++8mjxzcGFuPjEzMDwvc3Bhbj48L2RkPjwvZGw+PGRsPjxkdD48c3Bhbj48YSBocmVmPSIuLi9OZXdzL05ld0luZm8uYXNweD9pbmZvSWQ9MTUwMSI+6IuP5bee5biC56uL5Yy76Zmi5pys6YOo5YWz5LqO6ZOF6KGj562J6K6+5aSH5LiA5om5Li4uPC9hPjwvc3Bhbj48L2R0PjxkZCBjbGFzcz0icHJldmlldyI+6IuP5bee5Lit6L+c5oub5oqV5qCH5ZKo6K+i5pyJ6ZmQ5YWs5Y+45Y+X6IuP5bee5biC56uL5Yy76Zmi5pys6YOo55qE5aeU5omY77yM5bCx5YW26ZyA6KaB55qE6ZOF6KGj562J6K6+5aSH5LiA5om56L+b6KGM56ue5LqJ5oCn56OL5ZWG6YeH6LSt44CC5qyi6L+O5pyJ6LWE5qC855qE5L6b5bqU5ZWG5YmN5p2l5Y+C5Yqg5pys5qyh56ue5LqJ5oCn56OL5ZWG6YeH6LSt5rS75Yqo44CC5LiA44CB6YeH6LSt6aG555uu5qaC5Ya177yaMeOAgemHh+i0reWGheWuue+8mumTheiho+etieiuvuWkh+S4gOaJuSAuLi48L2RkPjxkZCBjbGFzcz0iaW5mbyI+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MDEiPuafpemYheWFqOaWhy4uLjwvYT7kvZzogIXvvJo8c3Bhbj7nrqHnkIblkZg8L3NwYW4+5Y+R6KGo5LqO77yaPHNwYW4+MjAyMy0zLTE1PC9zcGFuPiDngrnlh7vvvJo8c3Bhbj4xNzU8L3NwYW4+PC9kZD48L2RsPjxkbD48ZHQ+PHNwYW4+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MDAiPuiLj+W3nuW4guWQtOS4reWMuuS6uuawkeajgOWvn+mZouWFs+S6juWQtOS4reajgOWvny4uLjwvYT48L3NwYW4+PC9kdD48ZGQgY2xhc3M9InByZXZpZXciPuiLj+W3nuS4rei/nOaLm+aKleagh+WSqOivouaciemZkOWFrOWPuOWPl+iLj+W3nuW4guWQtOS4reWMuuS6uuawkeajgOWvn+mZoueahOWnlOaJmO+8jOWwseWFtumcgOimgeeahOWQtOS4reajgOWvn+mZouS4u+mimOepuumXtOaPkOWNh+mhueebrui/m+ihjOernuS6ieaAp+eji+WVhumHh+i0reOAguasoui/juaciei1hOagvOeahOS+m+W6lOWVhuWJjeadpeWPguWKoOacrOasoeernuS6ieaAp+eji+WVhumHh+i0rea0u+WKqOOAguS4gOOAgemHh+i0remhueebruamguWGte+8mjHjgIHph4fotK3lhoXlrrkuLi48L2RkPjxkZCBjbGFzcz0iaW5mbyI+PGEgaHJlZj0iLi4vTmV3cy9OZXdJbmZvLmFzcHg/aW5mb0lkPTE1MDAiPuafpemYheWFqOaWhy4uLjwvYT7kvZzogIXvvJo8c3Bhbj7nrqHnkIblkZg8L3NwYW4+5Y+R6KGo5LqO77yaPHNwYW4+MjAyMy0zLTEzPC9zcGFuPiDngrnlh7vvvJo8c3Bhbj4xNDk8L3NwYW4+PC9kZD48L2RsPjwvZGl2PmQCDQ8PFgQeCFBhZ2VTaXplAgoeC1JlY29yZGNvdW50AqsFZGRkUkxcZw93dWksqrUAgw1fosKSj6Q=',
                '__EVENTTARGET': 'aspPage',
                '__EVENTARGUMENT': page,
                '__EVENTVALIDATION': '/wEWEALVmr/oDgK3jbX7AwLLzNMbArC1xXMCrKHTowkCtZyP2AYCl4fJowIC3vKO7wYC6MKiYwKboK+bDALQ/ffbDALQ/evdDwLw6aKZDALw6ZqZDALw6aaZDAKmga7RCRdYS5G8XfvYQsl+56/KMlbPBtZK',
                'assPos': '',
                'hidC_id': 3,
                'hidPage': -1,
                'hidDivCss': 'manager1',
                'topCount': '',
                'Hidden2': '',
                'hID': '',
                'Hidden1': '',
                'Head2$hidType': 3,
                'Head2$FlashW': '',
                'Head2$FlashH': '',
                'Left1$HiddenField3': 1,
                'Left1$HiddenField1': 'dt280',
                'Left1$HiddenField2': '3|',
                'Leftusercol1$hidTeShuID': '',
                'aspPage_input': 1}
            text = tool.requests_post(url=self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            html = etree.HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//div[@class="newslist"]/dl')
            for li in detail:
                title = li.xpath('./dt/span/a/text()')[0]
                date_Today = li.xpath('./dd[2]/span[2]/text()')[0]
                href = li.xpath('./dt/span/a/@href')[0].replace('..', '')
                url = 'http://www.szzyztb.com/ShowASP' + href
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="conner"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//div[@class="conner"])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(t) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['body'] = item['body']
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '苏州中远招投标咨询有限公司'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal'] = title
        # print(item["body"])
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



