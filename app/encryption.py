import hashlib

#加密函数，md5加盐加密
def encryption(psw):
    m = hashlib.md5()
    salt1="今天首长不在家"#第一个盐
    salt2="大家一起码代码"#第二个盐
    m.update(salt1.encode("utf-8"))#在密码开头加第一个盐
    m.update(psw.encode()) #把字符串转换成bytes类型
    m.update(salt2.encode("utf-8"))#在密码末尾加第二个盐
    res=m.hexdigest()#返回摘要res，作为十六进制数据字符串值
    return res