#!/usr/bin/python

import os
import sys
import warnings
from setuptools import setup
from distutils.extension import Extension


# Use the current Mercurial revision as the package version.
from subprocess import check_output
rev = check_output(["hg", "id", "-n"]).strip()
version = 'hg-r' + rev
print "setup.py: Running on mercurial revision", rev


# Check to see if the user disabled code generation.
tryCodeGeneration = True
if '--no-generate' in sys.argv:
    sys.argv.remove('--no-generate')
    tryCodeGeneration = False

# If code generation wasn't explicitly disabled, try importing cythonize so we
# can enable code generation.
generateCode = False
if tryCodeGeneration:
    try:
        from Cython.Build import cythonize

    except ImportError:
        print "setup.py: You don't seem to have Cython installed. You can get"
        print "it from www.cython.org."
        print "setup.py: Continuing build using the last translated sources;"
        print "any updates to the .pyx files will be IGNORED."

    else:
        generateCode = True


def genCythonExtension(name, cythonSources, otherSources, **kwargs):
    """Helper function to generate a Cython-based extension definition.

    If Cython can be imported (see check above), return an Extension which uses
    Cython to generate C/C++ source files; otherwise, return an Extension which
    attempts to use pre-generated source files.

    """
    if generateCode:
        return Extension(
                name,
                otherSources + cythonSources,
                **kwargs
                )

    else:
        targetExtension = '.c'
        if kwargs.get('language', 'c') == 'c++':
            targetExtension = '.cpp'

        def translateCythonSourceFilename(cythonSource):
            if not cythonSource.endswith('.pyx'):
                warnings.warn("Cython source file %r doesn't end with '.pyx'!"
                        % (cythonSource, ),
                        RuntimeWarning
                        )

            translatedFilename = cythonSource.replace('.pyx', targetExtension)

            if not os.path.exists(translatedFilename):
                raise RuntimeError("Generated source file %r doesn't exist!"
                        % (translatedFilename, )
                        )

            return translatedFilename

        preGeneratedCythonSources = [
                translateCythonSourceFilename(sourceFile)
                for sourceFile in cythonSources
                ]

        return Extension(
                name,
                otherSources + preGeneratedCythonSources,
                **kwargs
                )


def genExt_pyrokit(setupKwargs):
    setupKwargs.setdefault('ext_modules', []).append(
            genCythonExtension(
                'pyrokit',
                [
                    'src/pyrokit.pyx',
                    ],
                [
                    'src/rocketInputHandler.cxx',
                    'src/ShellRenderInterfaceOpenGL.cpp',
                    'src/Panda3DSystemInterface.cpp',
                    'src/bootstrap.cpp',
                    ],
                language='c++',
                include_dirs=[
                    '/usr/include/panda3d',
                    'src',
                    ],
                library_dirs=[
                    '/usr/lib/panda3d',
                    ],
                libraries=[
                    'RocketCore',
                    'GL',
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
                )
            )


setupKwargs = dict(
        name='pyrokit',
        version=version,
        description='Bootstrap librocket from Python',
        author='whitelynx',
        author_email='whitelynx@gmail.com',
        license='MIT',
        url='http://bitbucket.org/skewedaspect/pyrokit',
        )

# Add enabled extensions
genExt_pyrokit(setupKwargs)

if generateCode and 'ext_modules' in setupKwargs:
    setupKwargs['ext_modules'] = cythonize(setupKwargs['ext_modules'])

# Make it a distribution!
setup(**setupKwargs)
