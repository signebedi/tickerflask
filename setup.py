from setuptools import setup, find_packages

def read_version():
    with open('tickerflask/__metadata__.py', 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")

version = read_version()

# # Read requirements.txt for install_requires
with open('requirements.txt', encoding="utf-8") as f:
    install_requires = f.read().splitlines()

setup(
    name='tickerflask',
    version=version,
    url='https://github.com/signebedi/tickerflask',
    author='Sig Janoska-Bedi',
    author_email='signe@atreeus.com',
    description='a yfinance flask wrapper API',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
