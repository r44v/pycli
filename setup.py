from setuptools import setup, find_packages

setup(
    name="pycli",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "openai", "colorama"],
    entry_points="""
        [console_scripts]
        pycli=pycli.main:cli
    """,
)
