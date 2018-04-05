mridata-python
==============
This is a python package for downloading and uploading datasets to mridata.org

Requirements
============
This package requires requests.

Installation
============

Go to the directory containing setup.py, then run

	python setup.py install

Usage
=====

After installing, you can upload to mridata directly from command line.

To upload GE dataset for example

	mridata upload_ge --anatomy Knee --fullysampled True P123456.7

The program will prompt you for username and password.
