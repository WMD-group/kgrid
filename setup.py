"""
kgrid: reciprocal-space sampling for ab-initio materials chemistry
"""

from os.path import abspath, dirname
from setuptools import setup, find_packages

project_dir = abspath(dirname(__file__))

setup(
    name='kgrid',
    version='1.0.0',
    description='Reciprocal space sampling for crystal structures',
    long_description="""
Generate reciprocal-space grids with scalar cutoff parameters and standard
crystal structure files. kgrid helps with k-point convergence problems when 
using ab initio codes that lack a single-parameter option, and help you
understand and plan calculations with codes that do.
""",
    url="https://github.com/WMD-group/kgrid",
    author="Adam J. Jackson / Walsh Materials Design group",
    author_email="a.j.jackson@physics.org",
    license='GPL v3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
        ],
    keywords='chemistry physics k-point sampling reciprocal',
    packages=find_packages(exclude=['test']),
    install_requires=['ase'],
    entry_points={
        'console_scripts': [
            'kgrid = kgrid.cli:main',
            'kgrid-series = kgrid.series:main'
            ]
        }    
    )
