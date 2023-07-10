import re

src='http://zjj.cangzhou.gov.cn/zjj/c100498/202306/54710f21df11449fbb177bbed0d62d63.shtml'
sss=re.findall(f'(.*/)[\w\d]+.shtml',src)
print(sss)
