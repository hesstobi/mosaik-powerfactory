from setuptools import setup, find_packages


setup(
    name='mosaik-powerfactory',
    version='0.2.0',
    author='Tobias Hess',
    author_email='tobias.hess at tu-dresden.de',
    description=('An adapter ti use Digsilent PowerFacotry with mosiak'),
    long_description=(open('README.rst').read() + '\n\n' +
                      open('CHANGES.rst').read() + '\n\n' +
                      open('AUTHORS.rst').read()),
    url='',
    install_requires=[
        'mosaik-api>=2.1',
        'arrow>=0.4.6'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mosaik-powerfactory-ldf = mosaik_powerfactory.ldf_simulator:main',
            'mosaik-powerfactory-rms = mosaik_powerfactory.rms_simulator:main'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
