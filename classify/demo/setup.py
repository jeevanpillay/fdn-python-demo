from distutils.core import setup, Extension
setup(name = 'demo', version = '1.0',  \
   ext_modules = [Extension('demo', ['loop.c', 'loop_api.c'])])
