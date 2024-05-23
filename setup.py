from setuptools import setup, find_packages

setup(
    name='pycli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'openai'
    ],
    entry_points='''
        [console_scripts]
        pycli=pycli.main:cli
    ''',
)
