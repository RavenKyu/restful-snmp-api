from setuptools import setup, find_packages

__version__ = '1.0.1'

LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

tests_require = [
    'pytest',
    'pytest-mock',
]

setup(
    name="restful-snmp-api",
    version=__version__,
    author="Duk Kyu Lim",
    author_email="hong18s@gmail.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    description='Restful SNMP API',
    url="https://github.com/RavenKyu/restful_snmp_api",
    license="MIT",
    keywords=["restful", "snmp", "api"],
    install_requires=[
        'flask==1.1.2',
        'PyYaml==5.4.1',
        'apscheduler==3.7.0',
        'easysnmp==0.2.5'
    ],
    tests_require=tests_require,
    package_dir={"restful_snmp_api": "restful_snmp_api"},
    packages=find_packages(
        where='.',
        include=['restful_snmp_api',
                 'restful_snmp_api.*'],
        exclude=['dummy-*', 'tests', 'tests.*']),
    package_data={
        "": ["*.cfg"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'restful-snmp-api=restful_snmp_api.__main__:main',
        ],
    },
    zip_safe=False,
)
