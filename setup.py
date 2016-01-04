#! user/bin/python
from setuptools import setup, find_packages
import sys, os
from glob import glob
import RouterCtrl

rc_doc = glob('doc/*')

setup(name='SeleniumRC',
      version=RouterCtrl.__version__,
      description="selenium_rc",
      packages=find_packages(where='.',exclude='test')+['selenium_rc.etc'], #['router_ctrl', 'serial_ctrl'],
      package_data = {'':['*.*']},
      include_package_data=True,
      py_modules = ['SeleniumRC'],
      zip_safe=False,
      data_files = [('doc', rc_doc),],
      )