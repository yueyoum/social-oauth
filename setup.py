from distutils.core import setup

import socialoauth

packages = [
    'socialoauth',
    'socialoauth.sites',
]


setup(
    name='socialoauth',
    version = socialoauth.VERSION,
    license = 'MIT',
    description = 'Python Package For SNS sites with OAuth2 support',
    long_description = open('README.txt').read(),
    author = 'Wang Chao',
    author_email = 'yueyoum@gmail.com',
    url = 'https://github.com/yueyoum/social-oauth',
    keywords = 'social, oauth, oauth2',
    packages = packages,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
