# -*- coding: utf-8 -*-
import ast
import os
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_init_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "itest", "__init__.py")
with open(_init_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='itest',
    version=version,
    description="Interface automation test framework",
    long_description="""itest is a python utility for doing easy, automation testing of http/https interface""",
    classifiers=[
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='interface automation testing',
    author='yinzhixin',
    author_email='',
    url='http://vdcoding.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'testreport','images']),
    include_package_data=True,
    zip_safe=False,
    install_requires=["gevent>=1.2.1", "requests>=2.13.0", "xlrd>=1.1.0", "tqdm>=4.19.5", "Jinja2>=2.9.6"],
    # test_suite="itest.test",
    # tests_require=['unittest2', 'mock'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'itest = itest.main:main',
        ]
    },
)

#build cmd: python .\setup.py bdist_wheel --universal
#upload cmd: twine upload dist/*