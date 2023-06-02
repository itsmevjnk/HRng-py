#!/usr/bin/env bash

echo "Compiling Python extensions..."
python3 setup.py build_ext --inplace

echo "Preparing libraries for PyInstaller..."
mv bpexec.so cybuild/
mv ua_list.so cybuild/

echo "Generating executable with PyInstaller..."
cd cybuild
pyinstaller --onefile --windowed -n bpexec --icon=dinobaka.ico run.py

echo "Cleaning up files..."
rm bpexec.so ua_list.so
cd ..