from __future__ import division, print_function
import os
import sys
from setuptools import setup
from setuptools import find_packages

PKG_NAME = 'limix_reader'
VERSION  = '0.0.1'

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def write_version():
    cnt = """
# THIS FILE IS GENERATED FROM %(package_name)s SETUP.PY
version = '%(version)s'
"""
    filename = os.path.join(PKG_NAME, 'version.py')
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'package_name': PKG_NAME.upper()})
    finally:
        a.close()

def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    write_version()

    install_requires = ['cffi>=1.0.0', 'bidict']
    setup_requires = ['cffi>=1.0.0']

    metadata = dict(
        name=PKG_NAME,
        version=VERSION,
        maintainer="Limix Developers",
        maintainer_email = "horta@ebi.ac.uk",
        license="BSD",
        url='http://pmbio.github.io/limix/',
        test_suite='setup.get_test_suite',
        packages=find_packages(),
        zip_safe=True,
        install_requires=install_requires,
        setup_requires=setup_requires,
        cffi_modules=["limix_reader/reader/plink/cbed/interface.py:ffi"],
    )

    if module_exists("distutils.command.bdist_conda"):
        from distutils.command.bdist_conda import CondaDistribution
        metadata['distclass'] = CondaDistribution
        metadata['conda_buildnum'] = 1
        metadata['conda_features'] = ['mkl']

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)

if __name__ == '__main__':
    if not module_exists("numpy"):
        print("Error: numpy package couldn't be found." +
              " Please, install it first so I can proceed.")
        sys.exit(1)

    setup_package()
