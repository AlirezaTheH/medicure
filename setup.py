import re
from os.path import join

from setuptools import find_packages, setup

packages = find_packages(exclude=['tests*'])

with open('requirements.txt') as f:
    requirements = f.read().split()

with open('README.md') as f:
    long_description = f.read()

with open(join('medicure', 'version.py')) as f:
    version_pattern = re.compile(r'__version__\s+=\s+\'(?P<version>.*)\'')
    version = re.search(version_pattern, f.read()).group('version')

setup(
    name='medicure',
    version=version,
    description=(
        'A cosmetic treatment for your media files: '
        'movies, tv shows and also their subtitles.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alirezatheh/medicure',
    project_urls={
        'Bug Tracker': 'https://github.com/alirezatheh/medicure/issues',
        'Documentation': 'https://github.com/alirezatheh/medicure',
        'Source Code': 'https://github.com/alirezatheh/medicure',
    },
    author='Alireza Hosseini',
    author_email='alirezatheh@gmail.com',
    packages=packages,
    entry_points={'console_scripts': ['medicure = medicure.cli:app']},
    keywords=[
        'nlp',
        'natural language processing',
        'information retrieval',
        'computational linguistics',
        'persian language',
        'persian nlp',
        'persian',
        'keyphrase extraction',
        'keyphrase extractor',
        'keyphrase',
        'keyword extraction',
        'keyword extractor',
        'keyword',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
    classifiers=[
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Other/Nonlisted Topic',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
    ],
)
