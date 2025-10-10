from setuptools import setup, find_packages

setup(
    name="Cryptotradelib",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # Core libraries
        "ccxt",
        "pandas",
        "pyarrow",
        "fastparquet",
        # Optional libraries for advanced scheduling and logging
        "schedule",
        "loguru",
    ],
    author="Jack Li",
    author_email="lij081923@gmail.com",
    description="A simple project for data handling and exchange interaction",
    url="https://github.com/SYSUljz/Cryptotradelib",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
