# Django Improved Permissions

[![Coverage Status](https://coveralls.io/repos/github/s-sys/django-improved-permissions/badge.svg?branch=master)](https://coveralls.io/github/s-sys/django-improved-permissions?branch=master)
[![Build Status](https://travis-ci.org/s-sys/django-improved-permissions.svg?branch=master)](https://travis-ci.org/s-sys/django-improved-permissions)
[![Documentation Status](https://readthedocs.org/projects/django-improved-permissions/badge/?version=latest)](http://django-improved-permissions.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/django-improved-permissions.svg)](https://badge.fury.io/py/django-improved-permissions)

---

## Overview

This is a fork of the original Django Improved Permissions package [here](https://github.com/s-sys/django-improved-permissions) that is maintained by Pluto Biosciences.

---

Django Improved Permissions (DIP) is a Django application made to make Django's default permission system more robust. Here are some highlights:

* Object-level Permissions
* Role Assignment
* Permissions Inheritance
* Cache
* Customizable Permissions per User Instance

## Documentation

Documentation for the original package is available [here](http://django-improved-permissions.readthedocs.io/en/latest/).

## Running locally

### First time set-up

Create a virtual environment in the top-level directory with `python3 -m venv env` and activate it with `source env/bin/activate`. Install requirements with `pip install -r permproject/requirements/reqs.txt`.

Make the test script executable with `chmod +x test.sh`.

### Running tests 

To run tests with coverage, run `./test.sh`. To just run the test suite, run `./manage.py test`.

## Contributing

Feel free to create new issues if you have suggestions or find some bugs.

## Commercial Support

This project is used in products of SSYS clients.

We are always looking for exciting work, so if you need any commercial support, feel free to get in touch: contato@ssys.com.br
