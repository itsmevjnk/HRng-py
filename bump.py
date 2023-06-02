#!/usr/bin/env python
# coding: utf-8

# Launcher/updater cho phần mềm check bump
# Nếu muốn public mã nguồn, vui lòng liên hệ tác giả tại:
#   itsmevjnk.work@gmail.com
#     hoặc
#   113ly.vinh.nguyenthanh@c3chuvanan.edu.vn

# prerequisites: pip install requests pyqt5

import os
import stat
import sys
import requests
import subprocess
import platform
from datetime import datetime
from PyQt5.QtWidgets import *
import traceback
import zipfile

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = os.open(os.devnull, os.O_RDWR)

workdir = os.path.expanduser("~/HRngTmp")

# exception hook
def exchook(exctype, value, tb):
    fname = datetime.now().strftime(workdir + "/bug-launcher-%d%m%Y_%H%M%S.txt")
    with open(fname, "w") as file:
        traceback.print_exception(exctype, value, tb, file = file)
    QMessageBox.critical(qt_win, "Lỗi", "Đã có lỗi xảy ra trong quá trình chạy.\nVui lòng gửi file {} cho tác giả qua email itsmevjnk.work@gmail.com.\nBấm OK để kết thúc chương trình.".format(fname.replace('/', os.path.sep)))
    sys.exit(-1)
sys.excepthook = exchook

qt_app = QApplication(sys.argv)
qt_win = QWidget()
qt_win_geo = qt_win.frameGeometry()
qt_win_cp = QDesktopWidget().availableGeometry().center()
qt_win_geo.moveCenter(qt_win_cp)
qt_win.move(qt_win_geo.topLeft())
qt_win.resize(1, 1)

# thoát khi cửa sổ đóng
def close_handler(event):
    event.accept()
    sys.exit(0)
qt_win.closeEvent = close_handler

# GUI cho cửa sổ tiến trình update
lyt_update = QVBoxLayout()
lyt_update.addWidget(QLabel("Đang tải phiên bản mới nhất..."))
pbr_update = QProgressBar()
lyt_update.addWidget(pbr_update)

os.makedirs(workdir, exist_ok = True) # tạo thư mục tạm chứa phần mềm và các file khác
os.chdir(workdir)

# tên file
exec_name = "bpexec"
osname = platform.system().lower()
if osname == "windows":
    exec_name += ".exe"
    plat_rel = platform.release()
    if plat_rel == "XP":
        osname += "_nt5"
    elif plat_rel == "Vista" or plat_rel == "7":
        osname += "_nt6"

# hàm chạy phần mềm và kết thúc
def launch():
    qt_win.hide()
    sys.exit(subprocess.call(os.path.join(workdir, exec_name), stdin=DEVNULL, stderr=DEVNULL, stdout=DEVNULL))

# link server update
if sys.argv[-1] == "local": url = "http://localhost/chkbump/rel/"
else: url = "https://itsmevjnk.mooo.com/hrng/rel/"

remote_ver = int(requests.get(url + "latest").content) # lấy phiên bản mới nhất

if os.path.exists(exec_name):
    local_ver = int(subprocess.check_output([os.path.join(workdir, exec_name), "-v"], encoding="ascii", stdin=DEVNULL, stderr=DEVNULL).strip())
    if remote_ver > local_ver:
        if QMessageBox.question(qt_win, "Thông báo cập nhật", "Đã có phiên bản mới của phần mềm.\nBạn muốn cập nhật không?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.No: launch()
    else: launch()

# tải update
qt_win.setLayout(lyt_update)
qt_win.show()
try:
    last_percent = 0
    with open("bpexec.zip", "wb") as f:
        resp = requests.get(url + str(remote_ver) + "/{}-{}.zip".format(osname, platform.machine().lower()), stream = True)
        total_len = resp.headers.get("content-length")
        if total_len is None: f.write(resp.content)
        else:
            dl = 0
            total_len = int(total_len)
            for data in resp.iter_content(chunk_size = total_len // 100):
                dl += len(data)
                f.write(data)
                percent = int((dl / total_len) * 100)
                if percent > last_percent:
                    last_percent = percent
                    pbr_update.setValue(percent)
                    qt_app.processEvents()
    with zipfile.ZipFile("bpexec.zip", "r") as zip:
        zip.extractall()
    os.remove("bpexec.zip")
    if not osname.startswith("windows"): os.chmod(os.path.join(workdir, exec_name), os.stat(os.path.join(workdir, exec_name)).st_mode | stat.S_IEXEC)
except: pass
qt_win.hide()
launch()
