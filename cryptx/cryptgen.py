import os
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import secrets
import PyInstaller.__main__


with open(input("Nhập file: "), "r", encoding="utf-8-sig") as fi:
    fi_data = fi.read()
    enckey = secrets.token_hex(16)
    iv = secrets.token_hex(16)
    print("Khoá mã hóa    : {}\nVector khởi tạo: {}".format(enckey, iv))
    cipher = AES.new(sha256(enckey.encode("ascii")).digest()[:32], AES.MODE_CBC, sha256(iv.encode("ascii")).digest()[:16])
    pld = b64encode(cipher.encrypt(pad(fi_data.encode("utf-8"), AES.block_size))).decode("ascii")
    imports = ""
    for line in fi_data.split('\n'):
        line.replace('\r', '')
        words = line.lower().split()
        if (len(words) > 1 and words[0] == "import") or (len(words) > 3 and words[0] == "from" and words[2] == "import"):
            print(line)
            imports += line + '\n'
    fdname = secrets.token_hex(4) + ".py"
    with open("cryptx.py", "r") as fs:
        with open(fdname, "w") as fd:
            fd.write(fs.read().format(enckey = enckey, iv = iv, pld = pld, imports = imports))
    PyInstaller.__main__.run([fdname, "--onefile", "--windowed", "--icon=dinobaka.ico"])
    os.remove(fdname)
    os.remove(fdname.replace(".py", ".spec"))