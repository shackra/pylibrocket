#!/usr/bin/python

import sys
from setuptools import setup
from distutils.extension import Extension


# Use the current Mercurial revision as the package version.
from subprocess import check_output
rev = check_output(["hg", "id", "-n"]).strip()
version = 'hg-r' + rev
print "setup.py: Running on mercurial revision", rev


def genExtensions(*pyrokitSources):
    return [Extension(
            'pyrokit',
            [
                'src/ShellRenderInterfaceOpenGL.cpp',
                'src/Panda3DSystemInterface.cpp',
                ] + list(pyrokitSources),
            language='c++',
            include_dirs=[
                'src',
                ],
            libraries=[
                'RocketCore',
                #TODO: How many of these are actually needed?
                'p3framework',
                'panda',
                'pandafx',
                'pandaexpress',
                'p3dtoolconfig',
                'p3dtool',
                'p3pystub',
                'p3direct',
                ],
            )]


def extensionsNoBuild():
    return genExtensions('src/pyrokit.cpp')


def extensionsBuild():
    try:
        from Cython.Build import cythonize

    except ImportError:
        print "setup.py: You don't seem to have Cython installed. You can get"
        print "it from www.cython.org."
        print "setup.py: Continuing build using the last translated sources;"
        print "any updates to the .pyx file will be IGNORED."
        return extensionsNoBuild()

    return cythonize(genExtensions('src/pyrokit.pyx'))


if '--nobuild' in sys.argv:
    sys.argv.remove('--nobuild')
    ext_modules = extensionsNoBuild()

else:
    ext_modules = extensionsBuild()


setup(name='pyrokit',
        version=version,
        description='Bootstrap librocket System and Render interfaces from Python',
        author='whitelynx',
        author_email='whitelynx@gmail.com',
        license='MIT',
        url='http://bitbucket.org/skewedaspect/pyrokit',
        ext_modules=ext_modules
        )
