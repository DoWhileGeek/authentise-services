import re
import subprocess
import contextlib
import os
import json

from setuptools import setup

VERSION_FILE = os.path.join(os.path.dirname(__file__), "authentise_services/version.json")


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
    with open(VERSION_FILE) as version_file:
        return json.loads(version_file.read())["version"]


@contextlib.contextmanager
def write_version():
    git_description = _get_git_description()

    version = _create_version_from_description(git_description) if git_description else None

    if version:
        with open(VERSION_FILE, 'w') as version_file:
            version_file.write(json.dumps({"version": version}))
    yield


def main():
    with write_version():
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
