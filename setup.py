from setuptools import setup

setup(
    name='autodoist',
    version='0.0.1',
    py_modules=['autodoist'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        autodoist=autodoist:cli
    ''',
)
