import setuptools
from env import ROOT_DIR
from os import mkdir

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='survey_route_generation',
                 packages=['survey_route_generation'],
                 install_requires=install_requires)

mkdir(ROOT_DIR + "\\output")
mkdir(ROOT_DIR + "\\output\\data")
mkdir(ROOT_DIR + "\\output\\logs")
mkdir(ROOT_DIR + "\\output\\results")
