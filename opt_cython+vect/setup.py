from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy as np

setup(cmdclass={'build_ext' : build_ext}, 
        include_dirs = [np.get_include()],
        ext_modules = cythonize('location.pyx'))
setup(cmdclass={'build_ext' : build_ext}, 
        include_dirs = [np.get_include()],
        ext_modules = cythonize('agent.pyx'))
setup(cmdclass={'build_ext' : build_ext}, 
        include_dirs = [np.get_include()],
        ext_modules = cythonize('transition.pyx'))
