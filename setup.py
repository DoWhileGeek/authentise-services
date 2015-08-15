import re
import subprocess

from setuptools import setup


def _get_git_description():
    try:
        return subprocess.check_output(["git", "describe"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None


def _create_version_from_description(git_description):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git_description)
    if not match:
        version = git_description
    else:
        version = "{tag}.post{offset}".format(**match.groupdict())
    return version


def get_version():
    description = _get_git_description()

    return _create_version_from_description(description)


def main():
    setup(
        name="authentise_services",
        url="https://github.com/DoWhileGeek/authentise-services",
        description="A client library for Authentise open services",
        author="Joeseph Rodrigues",
        author_email="dowhilegeek@gmail.com",
        version=get_version(),
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


if __name__ == "__main__":
    main()
