from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import binascii

class NavicatPasswordDecoder:
    @staticmethod
    def decrypt_password(encrypted_password):
        try:
            if not encrypted_password:
                return ""
                
            # Navicat 11/12使用的密钥
            key = b"libcckeylibcckey"
            iv = b"libcciv libcciv "
            
            # 将十六进制字符串转换为字节
            try:
                encrypted_data = binascii.unhexlify(encrypted_password)
            except binascii.Error:
                try:
                    # 如果不是十六进制，尝试base64解码
                    encrypted_data = base64.b64decode(encrypted_password)
                except Exception:
                    return "解密失败: 无效的密码格式"
            
            # 创建解密器
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # 解密
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # 移除PKCS7填充
            padding_length = decrypted_data[-1]
            if padding_length > len(decrypted_data):
                return "解密失败: 无效的填充"
                
            decrypted_password = decrypted_data[:-padding_length]
            
            # 尝试不同的编码方式解码
            encodings = ['utf-8', 'ascii', 'latin1']
            for encoding in encodings:
                try:
                    result = decrypted_password.decode(encoding)
                    if result:
                        return result
                except UnicodeDecodeError:
                    continue
                    
            return "解密失败: 无法解码密文"
            
        except Exception as e:
            return f"解密失败: {str(e)}" 