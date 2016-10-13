# -*- coding: UTF-8 -*-
__author__ = 'MD'

import base64
import binascii

from M2Crypto.EVP import Cipher

OP_ENCRYPT = 1  # 加密操作
OP_DECRYPT = 0  # 解密操作

# 去掉填充部分
unpad = lambda s: s[0:-ord(s[-1])]


def ase_html_data_decrypt(data):
    """
    解密html请求的AES加密数据
    :param data: 数据base64编码
    :return:解密后的字符串，如果为无效字符串则返回空字符串
    """
    # 定义cipher解密器
    key = '!@#$%^&*()_+|%^&'  # 一个字符占一个byte字节，一个byte字节等于8bit位，这里16个字符占128位
    iv = '!@#$%^&*()_+|%^&'   # 初始化向量，用于避免相同的书多次加密产生同样的密文
    # 使用aes_128_ecb算法对数据解密,128位（4*4字节）算法，不够位的用0填充
    decryptor = Cipher(alg='aes_128_cbc', key=key, iv=iv, op=OP_DECRYPT, padding=0)
    # 数据解码（base64解码，编码都是asicii形式）
    encrypt_data = base64.b64decode(data)
    # 数据解密
    decrypted_data = decryptor.update(encrypt_data)
    decrypted_data += decryptor.final()
    del decryptor  # 需要删除

    # 前台的数据采用Pkcs7方式进行填充，后面填充的字节为该字节序列的长度,所以要把填充的部分去掉
    return unpad(decrypted_data)

