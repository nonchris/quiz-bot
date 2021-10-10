from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

pkgs = find_packages(where='.')

setup(
    name='discord-quiz-bot',
    version='1.1.0',
    description='A quiz-bot for discord',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nonchris/quiz-bot/',
    author='nonchris',
    author_email='info@nonchris.eu',

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Other Audience',
        'Topic :: Communications :: Chat',

        'Typing :: Typed',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='discord-bot, quiz',

    package_dir={'': '.'},

    packages=find_packages(where='.'),

    python_requires='>=3.8, <4',

    install_requires=['dateparser~=1.0.0',
                      'discord.py ~= 1.7.2'],

    entry_points={
        'console_scripts': [
            'quiz-bot=src:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/nonchris/quiz-bot/issues',
        'Source': 'https://github.com/nonchris/quiz-bot/',
    },
)
