from setuptools import setup
from setuptools import find_packages

setup(name='learntools',
      version='0.1',
      description='Utilities for Kaggle Learn exercises',
      url='http://github.com/kaggle/learntools',
      author='Dan Becker',
      author_email='dan@kaggle.com',
      license='Apache 2.0',
      packages=find_packages(),
      zip_safe=True)
