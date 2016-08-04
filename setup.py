#! /usr/bin/env python

"""

"""

from setuptools import find_packages, setup
import hesysopt

setup(name='hesysopt',
      version=hesysopt.__version__,
      url='http://github.com/znes/HESYSOPT',
      author='Simon Hilpert',
      author_email='simon.hilpert@hs-flensburg.de',
      description='HESYSOPT - Open source heating system optimization tool.',
      namespace_package = ['hesysopt'],
      packages=find_packages(),
      package_dir={'hesysopt': 'hesysopt'},
      install_requires=['oemof >= 0.0.9',
                        'numpy >= 1.7.0',
                        'pandas >= 0.17.0',
                        'pyomo >= 4.2.0, != 4.3.11377']
     )
