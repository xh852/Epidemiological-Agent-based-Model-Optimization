from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize('location.pyx'))
setup(ext_modules = cythonize('agent.pyx'))
setup(ext_modules = cythonize('transition.pyx'))
