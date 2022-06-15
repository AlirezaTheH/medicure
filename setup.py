import re
from pathlib import Path

from setuptools import find_packages, setup

packages = find_packages(exclude=['tests*'])

requirements_path = Path('requirements')
with open(requirements_path / 'main.txt') as f:
    requirements = f.read().split()

extras_requirements = {}
for extra in requirements_path.iterdir():
    if not extra.name.endswith('main.txt'):
        with open(extra) as f:
            extras_requirements[extra.name[:-4]] = f.read().split()

with open('README.md') as f:
    long_description = f.read()

with open(Path('medicure') / 'version.py') as f:
    version = re.search(
        r'__version__\s=\s\'(?P<version>.*)\'', f.read()
    ).group('version')

setup(
    name='medicure',
    version=version,
    description=(
        'A cosmetic treatment for your media files: '
        'movies, TV shows and also their subtitles.'
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
    package_data={'medicure': ['*.patch']},
    entry_points={'console_scripts': ['medicure = medicure.cli:app']},
    keywords=[
        'audio',
        'video',
        'videos',
        'media',
        'multimedia',
        'movies',
        'tv',
        'tvshows',
        'tv-shows',
        'series',
        'subtitle',
        'subtitles',
        'audio-processing',
        'video-processing',
    ],
    install_requires=requirements,
    extras_require=extras_requirements,
    python_requires='>=3.8',
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
