from distutils.core import setup
from setuptools import find_packages

requires = ['tornado', 'sqlalchemy', 'configparser', 'schedule']

setup(
    name='Proyecto Asistencia Elfec',
    version='1',
    packages=find_packages(),
    url='',
    license='Licence',
    author='Berthy Vargas Villarreal',
    author_email='bvargas@cloudbit.com.bo',
    description='Server Base on Tornado framework',
    install_requires=requires
)