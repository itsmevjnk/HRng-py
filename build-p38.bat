@echo off

echo [32-bit compilation]

echo Compiling Python extensions...
"C:\Program Files (x86)\Python38-32\python.exe" setup.py build_ext --inplace

echo Preparing libraries for PyInstaller...
move bpexec.pyd cybuild
copy bump.py cybuild

echo Generating executables with PyInstaller...
cd cybuild
"C:\Program Files (x86)\Python38-32\Scripts\pyinstaller.exe" --onefile --windowed -n bpexec run.py
"C:\Program Files (x86)\Python38-32\Scripts\pyinstaller.exe" --onefile --windowed -n HRng bump.py

echo Creating archives...
cd dist
7z a -tzip ..\..\windows_nt6-x86.zip bpexec.exe
7z a -tzip ..\..\HRng-windows_nt6.zip HRng.exe
del bpexec.exe HRng.exe
cd ..

echo Cleaning up files...
del bpexec.pyd bump.py
rd /s /q build dist
cd ..



echo [64-bit compilation]

echo Compiling Python extensions...
"C:\Program Files\Python38\python.exe" setup.py build_ext --inplace

echo Preparing libraries for PyInstaller...
move bpexec.pyd cybuild
copy bump.py cybuild

echo Generating executables with PyInstaller...
cd cybuild
"C:\Program Files\Python38\Scripts\pyinstaller.exe" --onefile --windowed -n bpexec run.py
"C:\Program Files\Python38\Scripts\pyinstaller.exe" --onefile --windowed -n HRng bump.py

echo Creating archives...
cd dist
7z a -tzip ..\..\windows_nt6-amd64.zip bpexec.exe
7z a -tzip ..\..\HRng-win64_nt6.zip HRng.exe
del bpexec.exe HRng.exe
cd ..

echo Cleaning up files...
del bpexec.pyd bump.py
rd /s /q build dist
cd ..

