# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Forklyft - Onling food ordering and rating",
    author_email="utkarsh.mask@gmail.com",
    url="",
    keywords=["Swagger", "Forklyft - Onling food ordering and rating"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    This API performs fetch instructions to retrieve information from the database of food items, restaurants, users and orders. It incoporates various attributes such as ratings, prices, addresses, food-categories and decriptions etc  This is the first version of the API
    """
)
