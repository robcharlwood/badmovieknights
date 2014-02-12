# Bad Movie Knights — Django API
[![Build Status](https://travis-ci.org/robcharlwood/badmovieknights.png?branch=master)](https://travis-ci.org/robcharlwood/badmovieknights) [![Coverage Status](https://coveralls.io/repos/robcharlwood/badmovieknights/badge.png?branch=master)](https://coveralls.io/r/robcharlwood/badmovieknights?branch=master)

This repository contains the entire django API for the Bad Movie Knights website.

The codebase is designed to run on Google App Engine. This is why the libs directory contains a few local copies of the 3rd party depedencies that this source code requires. Mainly the wonderful ``djangorestframework`` and some other helper libs such as ``markdown``, ``django-taggit`` and ``django-filters``.

The codebase also includes a customised local version of ``South``.
This is so that I could update it to recognise Google's CloudSQL database backend.
