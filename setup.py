from setuptools import setup

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="authentise_services",
    url="https://github.com/DoWhileGeek/authentise-services",
    description="A client library for Authentise open services",
    long_description=long_description,
    author="Joeseph Rodrigues",
    author_email="dowhilegeek@gmail.com",
    version="0.3.0",
    packages=["authentise_services"],
    package_data={"authentise_services": ["authentise_services/*"], },
    include_package_data=True,
    install_requires=[
        "requests==2.7.0",
    ],
    extras_require={
        'develop': [
            'pylint==1.4.3',
            'pytest==2.6.4',
            'httpretty==0.8.10',
            'twine==1.5.0',
        ]},
)
