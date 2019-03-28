from setuptools import setup
from setuptools import find_packages


setup(
    name="sharpener",
    version="0.1.0",
    package_dir='src',
    packages=find_packages('src'),
    tests_require=[
        'pytest',
    ],
    install_requires=[
        'click',
        'pillow',
    ],
)
