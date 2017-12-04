# From irradiation to decay
This tool aims at post-processing files containing isotopes and elements irradiation and decay states, in order to generate decay power curves and source terms inventories.

## Getting started
This tool runs with Python v3.5. To run it:
```
python main.py
```
A GUI application using tkinter module then leads the move.

## Tests
Two kind of tests have been implemented:
- unit tests within the docstrings of the elementary functions in functions.py
- global tests checking the good behaviour of the entire tool
The tests can be run with the following command:
```
py.test --doctest-module -v
```

## Author
* **theo43** - [Github](https://github.com/theo43)

