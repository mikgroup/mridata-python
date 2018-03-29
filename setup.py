from setuptools import setup

setup(name='mridata',
      version='0.1',
      description='Python package for downloading and uploading to mridata.org.',
      url='http://github.com/mikgroup/mridata-python',
      author='Frank Ong',
      author_email='frankong@berkeley.edu',
      license='BSD',
      scripts=['bin/mridata'],
      install_requires=[
          'requests',
      ]
)
