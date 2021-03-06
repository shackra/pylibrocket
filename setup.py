#!/usr/bin/env python2
# encoding: utf-8

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
    
    
def genExt_pylibrocket(setupKwargs):
    setupKwargs.setdefault('package_dir', {})['pylibrocket'] = 'src'
    setupKwargs.setdefault('packages', []).append('pylibrocket')
    
    setupKwargs.setdefault('ext_modules', []).append(
            genCythonExtension(
                'pylibrocket.rocket_init',
                [
                    'src/rocket_init.pyx',
                    ],
                [],
                language='c++',
                libraries=[
                    'RocketCore',
                    ],
                )
            )
    
    
def genExt_pylibrocket_opengl(setupKwargs):
    setupKwargs.setdefault('ext_modules', []).append(
            genCythonExtension(
                'pylibrocket.opengl',
                [
                    'src/opengl/opengl.pyx',
                    ],
                [
                    'src/opengl/ShellRenderInterfaceOpenGL.cpp',
                    'src/opengl/bootstrap.cpp',
                    ],
                language='c++',
                include_dirs=[
                    'src',
                    ],
                libraries=[
                    'RocketCore',
                    'GL',
                    ],
                )
            )
    
    
def genExt_pylibrocket_panda3d(setupKwargs):
    setupKwargs.setdefault('ext_modules', []).append(
            genCythonExtension(
                'pylibrocket.panda3d',
                [
                    'src/panda3d/panda3d.pyx',
                    ],
                [
                    'src/panda3d/rocketRenderInterface.cxx',
                    'src/panda3d/rocketInputHandler.cxx',
                    'src/panda3d/Panda3DSystemInterface.cpp',
                    'src/panda3d/bootstrap.cpp',
                    ],
                language='c++',
                #TODO: Remove the need for the explicit panda3d include dir
                # here; instead, #include statements should be including
                # "panda3d/___.h".
                include_dirs=[
                    '/usr/include/panda3d',
                    'src',
                    ],
                #TODO: Make this more cross-platform!
                library_dirs=[
                    '/usr/lib/panda3d',
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
                )
            )
    
    
def genExt_pylibrocket_sfml(setupKwargs):
    setupKwargs.setdefault('ext_modules', []).append(
            genCythonExtension(
                'pylibrocket.sf',
                [
                'src/sf/sf.pyx',
                    ],
                [
                    'src/sf/RenderInterfaceSFML.cpp',
                    'src/sf/SystemInterfaceSFML.cpp',
                    ],
                language='c++',
                include_dirs=[
                    'src',
                    ],
                libraries=[
                    'RocketCore',
                    'sfml-graphics',
                    'sfml-window',
                    'sfml-system',
                    ],
                )
            )
    
    
setupKwargs = dict(
        name='pylibrocket',
        version=version,
        description='Bootstrap librocket from Python',
        author="Shackra Sislock",
        #author='whitelynx',
        author_email="jorgean@lavabit.com",
        #author_email='whitelynx@gmail.com',
        license="LGPL3",
        #license='MIT',
        url="https://bitbucket.org/shackra/pylibrocket",
        #url='http://bitbucket.org/skewedaspect/pyrokit',
        )

# Add enabled extensions
genExt_pylibrocket(setupKwargs)
genExt_pylibrocket_opengl(setupKwargs)
#genExt_pylibrocket_panda3d(setupKwargs) # Ignoramos la integración con Panda3D
genExt_pylibrocket_sfml(setupKwargs)

if generateCode and 'ext_modules' in setupKwargs:
    setupKwargs['ext_modules'] = cythonize(setupKwargs['ext_modules'])
    
# Make it a distribution!
setup(**setupKwargs)
