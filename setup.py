#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "libserial",
    version = "1.0",
    description="Python Serial Port Utility Classes",
    author="John Stowers",
    author_email="john.stowers@gmail.com",
    url="http://github.com/nzjrs/libserial/tree/master",
    package_dir = {"libserial" : ""},
    packages = ["libserial"]
)

