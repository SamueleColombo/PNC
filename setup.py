try:
    # Try to import the setup from the default distutils module.
    from distutils.core import setup
except ImportError:
    # If it fails import the setup function from the setuptoools module.
    from setuptools import setup


setup(
    name='PNC',
    version='0.1',
    packages=['pnc', 'tests'],
    url='http://github.com/SamueleColombo/PNC',
    license='',
    author='Samuele Colombo',
    author_email='s.colombo003@studenti.unibs.it',
    description='',
    requires=['tensorflow==1.2']
)
