from setuptools import find_packages, setup
from os.path import join, dirname

setup(
    name="expense_report",
    version='1.0',
    package_dir={"": "src"},
    packages=find_packages(exclude=['config,static,templates']),
    zip_safe=True,
    decription='',
    entry_points={}
)
