import logging
import sys

import requests


logger = logging.getLogger(__name__)
s = requests.Session()
cookie_str = "__mtxcar=(direct):(none); __mtxsd=dacfbccf.1517303973187.0.1; __mtxud=3f930e11fba3f8ca.1509439473214.1517222149074.1517303973182.66; sd=Z_mT626EeNkoe23Tf3q5YK0xDAKLwQdDjtE7IWbwWnfbBhc7phJL1aGcw8KLsRTkm0iZaPFB-yCa_G9_qZb-SxHEZM9VGhXLKDvJ4Gl6eHA; uuid=NIRUoO5ET8O2IQIhySKI_g; wx_pw=oZDRm43JsKy6pujw532iBj13g1uS*ix9QjfuOk5A8XpZ3fQjfyY7Id1w24T9Xci42yZTnjcbvhfG6ykaNmZLJCh3PC-IkQ73o-FZpnEfrQqvKb4ji0LRIz6PdMvpFnea2XfMIvAfzY70ubXz5LmiRAutbx4qafzMbIFrsWFPd-RciRO2loe4xaLxAzN*cx*Pz*anL6BQoJHsXxrl58fIESuGCS-UIEsA84sG4X850Vh8qiytL5Q-AqFEzHSfC09aP*xqUBTdUtns9bYB4Jw4aeuxCreddim*LZ4oHuyNETDIyflGTWWStMQ90Oh9FI5Q; __mtxsr=csr:(direct)|cdt:(direct)|advt:(none)|camp:(none)"
cookie_list = cookie_str.split(';')
for c in cookie_list:
    name, value = c.split('=')
    if name == 'wx_pw':
        s.cookies[name] = 'helloworld'
    s.cookies[name] = value
header = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.5.20 NetType/WIFI Language/zh_CN",
    "Referer": "http://event.wanmei.com/csgo/wxplatform/index?param=1"
}

s.headers = header

auth_rsp = s.get("https://passport.wanmei.com/api/wxjs.do?method=auth&jsonpCallback=wx.auth_jsonp&url=http%3A%2F%2Fevent.wanmei.com%2Fcsgo%2Fwxplatform%2Findex%3Fparam%3D1&aid=3")
print(auth_rsp.content)
print(s.cookies)
print(s.headers)
sign_rsp = s.get("http://event.wanmei.com/csgo/wxplatform/sign?r=0.029192996882969946")
print(sign_rsp.elapsed)
print(sign_rsp.content)
print(s.cookies)
print(s.headers)
