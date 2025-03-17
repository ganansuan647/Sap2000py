from setuptools import find_packages, setup

__version__="0.1.5"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Sap2000py",
    version=__version__,
    description="Sap2000 API python interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lingyun Gou",
    author_email="17717910647@163.com",
    url="https://github.com/ganansuan647/Sap2000py",
    license="GPL Licence",
    keywords="Sap2000 API python",
    python_requires=">=3.9.0",
    package_dir={"": "Sap2000py"},
    packages=find_packages("Sap2000py"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        "numpy",
        "comtypes>=1.1.11",
        "loguru",
        "pathlib",
        "rich",
        "sectionproperties>=3.3.0",
    ],
)
