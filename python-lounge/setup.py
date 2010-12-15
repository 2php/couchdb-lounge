#!/usr/bin/env python

from distutils.core import setup

py_packages = ['lounge', 'lounge.client']

description = 'lounge python module'
long_description = 'nice interface to lounge configuration'

setup( version = '1.4.0',
	   description = description,
	   long_description = long_description,
	   name = 'python-lounge1',
	   author='meebo',
	   author_email='shaun@meebo.com',
	   url='http://tilgovi.github.com/couchdb-lounge/',
	   packages = py_packages)
