from setuptools import setup, find_packages

setup(
    name='domain_package',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
)