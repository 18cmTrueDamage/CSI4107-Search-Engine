from setuptools import setup

setup(
    name='Vanilla',
    version='1.0',
    description='A Search Engine',
    author='Justin',
    author_email='',
    license='MIT',
    url='',
    packages=['src'],
    install_requires=['nltk', 'bs4', 'numpy',
                      'lxml', 'PyQt5', 'PyQt5-sip',
                      'six', 'soupsieve', 'beautifulsoup4']
)
