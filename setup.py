"""The setup script."""

import os.path

from setuptools import find_packages, setup

import versioneer

with open("requirements.txt") as install_requires_file:
    install_requires = install_requires_file.read().splitlines()

with open("requirements-dev.txt") as dev_requires_file:
    dev_requires = dev_requires_file.read().splitlines()

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()


def find_package_data(*paths):
    return [
        os.path.normpath(os.path.join("..", p, f))
        for path in paths
        for (p, d, fs) in os.walk(path)
        for f in fs
    ]


setup(
    name="organizer",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Rustle Karl",
    author_email="fu.jiawei@outlook.com",
    url="https://github.com/fujiawei-dev/organizer",
    description="Automatically organize video files.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    keywords="organizer",
    license="MIT license",
    packages=find_packages(
        include=["organizer", "organizer.*"],
        exclude=("tests", "tests.*", "docs"),
    ),
    test_suite="tests",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "organizer=organizer.cli:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
    ],
)
