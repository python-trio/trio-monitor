from setuptools import setup, find_packages

exec(open("trio_monitor/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="trio-monitor",
    version=__version__,
    description="A monitor utility for Trio",
    url="https://github.com/python-trio/trio-monitor.git",
    long_description=open("README.rst").read(),
    author="Laura F. Dickinson",
    author_email="l@veriny.tf",
    license="MIT -or- Apache License 2.0",
    packages=find_packages(),
    install_requires=[
        "trio",
    ],
    keywords=[
        # COOKIECUTTER-TRIO-TODO: add some keywords
        # "async", "io", "networking", ...
    ],
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",

        # COOKIECUTTER-TRIO-TODO: Consider adding trove classifiers for:
        #
        # - Development Status
        # - Intended Audience
        # - Topic
        #
        # For the full list of options, see:
        #   https://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
)
