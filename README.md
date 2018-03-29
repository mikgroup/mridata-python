mridata
========
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

After installing, there will be a binary callable from terminal.

To upload GE dataset for example

	mridata upload_ge --anatomy Knee --fullysampled True P123456.7
