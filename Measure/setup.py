from setuptools import setup, Extension

module = Extension('mymodule', sources=['mymodule.c'])

setup(
    name='mymodule', 
    version='0.1', 
    description='This is an immortal instance testbed.', 
    ext_modules=[module]
)

