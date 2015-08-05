from setuptools import setup


setup(
    name="authentise_services",
    description="A client library for Authentise open services",
    author="Joeseph Rodrigues",
    author_email="dowhilegeek@gmail.com",
    version="0.1.0",
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
        ]},
)
