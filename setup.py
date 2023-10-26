# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in rezappte/__init__.py
from rezappte import __version__ as version

setup(
	name='rezappte',
	version=version,
	description='An app to manage your recipes and share them with your friends. With additional functions.',
	author='Ivanios',
	author_email='gokuflynn@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
