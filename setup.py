""" improved_permissions setup configs """
import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-improved-permissions',
    version='0.3.0',
    packages=[
        'improved_permissions',
        'improved_permissions.migrations',
        'improved_permissions.templatetags',
    ],
    include_package_data=True,
    license='MIT License',
    description='A Django app to handle all kinds of permissions and roles.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/pluto-biosciences/django-improved-permissions',
    author='Pluto Biosciences (fork of S-SYS)',
    author_email='engineering@plutobio.com',
    python_requires='>=3.10',
    install_requires=[
        'Django>=4.2,<6.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
