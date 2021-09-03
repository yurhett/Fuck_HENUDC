from pyDes import des, CBC, PAD_PKCS5
import base64

# 秘钥
KEY = 'b3L26XNL'

def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    s = base64.b64decode(s)
    secret_key = KEY
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    decrypt_str = des_obj.decrypt(s, padmode=PAD_PKCS5)
    return decrypt_str

print(des_descrypt(''))