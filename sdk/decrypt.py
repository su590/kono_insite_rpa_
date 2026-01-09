from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def aes(text: str, key: bytes = b"iPNzWh5ggqtpcOYs") -> str:
    return unpad(AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(text)), AES.block_size, style='pkcs7').decode('utf-8')
