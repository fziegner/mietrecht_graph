from setuptools import setup

setup(
    name='bauprofessor_crawler',
    version='0.0',
    packages=['BauGraph'],
    url='https://git.informatik.uni-leipzig.de/dmw/civil_engineering/bauprofessor_crawler.git',
    license='',
    author='Janos Borst',
    author_email='',

    install_requires=["scrapy","spacy","pdftotext",
              "tqdm",
              "networkx",
              "python-igraph"],
    description='A package to generate a knowledge graph for the construction industry. (German)'
)
