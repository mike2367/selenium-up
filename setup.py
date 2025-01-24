from setuptools import find_packages, setup

setup(
    name='seleniumUp',          # Required
    version='0.1.0',           # Required
    packages=find_packages(),  # Required
    include_package_data=True,  # Includes package data as specified below
    package_data={
        'seleniumUp': ['resources/**/*'],  # Includes all files in the resources folder
    },
)