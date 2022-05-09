# Survey route generation

A study project for survey generation route of geographical coordinates using genetic algorithm.

## Installation
Use command to install dependencies:

``
pip install -r requirements.txt
``

## Compilation

To compile python to exe for dev use command:

``
python -m nuitka main.py
``

To compile python to exe for prod use command:

``
python -m nuitka main.py --standalone --enable-plugin=numpy
``