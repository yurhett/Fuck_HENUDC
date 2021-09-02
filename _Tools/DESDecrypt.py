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

print(des_descrypt('6XkC1UAk07fK0uTaGPUu77i/+r7j/o1JQ/XygRxee2LMiX5H+w/BOlgBGXJ4 SffK1rZ+7Ls/vCLzlOoLWsauNtTeqlazZ2uUMDVlhrZTxA5dknDNirB3uvVC sv4GH/EX82nHiibHYU4iFs3hnIj+6Q+hWaYxzXtjC+VmT2XIPIv/sh8M3i6t nvROntJyD1p54nxzL9gatbx+iscXRJ7OEVIm483fLTYK6B0cFuj+HSsAWM0U ZPFErEyhIcwmwvnK'))