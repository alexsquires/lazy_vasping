"""This is a setup.py script to install lazy_vasping"""

import os
import glob

from setuptools import setup, find_packages

SETUP_PTH = os.path.dirname(os.path.abspath(__file__))

def readme():
    """
    Set GitHub repo README as package README.
    """
    with open("README.md") as readme_file:
        return readme_file.read()

scripts = ['lv_static','lv_parse', 'lv_wrangle', 'lv_submit', 'lv_scrape', 'lv_store']

setup(
    name="lazy_vasping",
    packages=find_packages(),
    version="0.0.1",
    install_requires=[
        "vasppy",
        "pandas",
        "pymatgen",
    ],
    author="Alex Squires",
    author_email="ags49@bath.ac.uk",
    maintainer="Alex Squires",
    maintainer_email="ags49@bath.ac.uk",
    url="https://github.com/alexsquires/lazy_vasping",
    long_description=readme(),
    long_description_content_type="text/markdown",
    package_data= {"lazy_vasping":["errors.yaml"]},
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    license="MIT",
    entry_points={'console_scripts':[f'{s} = cli.{s}:main' for s in scripts]}
)
