import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='survey_route_generation',
                 packages=['survey_route_generation'],
                 install_requires=install_requires)
