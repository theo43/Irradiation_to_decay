***************************
Presentation of the program
***************************

Introduction
************

This tool aims at post-processing files containing isotopes and elements irradiation and decay states, in order to generate decay power curves and source terms inventories.

Getting started
***************

This tool runs with Python v3.5 or more. To run it:

``python main.py``

A GUI designed with `tkinter` module then controls the application.

Tests
*****

Two kind of tests have been implemented:

- Unit tests within the docstrings of the elementary functions in `functions.py`
- Global tests checking the good behaviour of the entire tool

The tests can be run with the following command:

``py.test --doctest-module -v``

Sphinx documentation
********************

The documentation is automated with Sphinx. To generate the documentation, go to the `sphinx` folder, and run:

``make html``

This generated the `build/html/index.html' file which can be displayed with the following command:

``firefox index.html``
