# From https://github.com/Lucky-Mano/Poetry_C_Extension_Example

from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

from setuptools import Extension
from setuptools.command.build_ext import build_ext

import numpy


extensions = [
    Extension("ttt.core.convert", sources=["src/ext/to_blocks.c"]),
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            pass

    def build_extension(self, ext):
        try:
            ext.include_dirs.insert(0, numpy.get_include())
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            pass


def build(setup_kwargs):
    setup_kwargs.update({"ext_modules": extensions, "cmdclass": {"build_ext": ExtBuilder}})
