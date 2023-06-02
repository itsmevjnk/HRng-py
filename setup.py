import setuptools
from distutils.core import Extension, setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils import sysconfig
import os

class NoSuffixBuilder(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        return filename.replace(suffix, "") + ext

setup(ext_modules=cythonize(["bpexec.py"]), cmdclass={"build_ext": NoSuffixBuilder})