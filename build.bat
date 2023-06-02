@echo off

echo Compiling Python extensions...
python setup.py build_ext --inplace

echo Preparing libraries for PyInstaller...
move bpexec.pyd cybuild
copy bump.py cybuild

echo Generating executables with PyInstaller...
cd cybuild
pyinstaller --onefile --windowed -n bpexec run.py
pyinstaller --onefile --windowed -n HRng bump.py

echo Cleaning up files...
del bpexec.pyd bump.py
cd ..