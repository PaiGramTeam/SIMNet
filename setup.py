"""Run setuptools."""

from pathlib import Path

from setuptools import find_packages, setup

from simnet.version import __version__


def get_requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with Path("requirements.txt").open() as reqs:
        for install in reqs:
            if install.startswith("#"):
                continue
            requirements_list.append(install.strip())

    return requirements_list


def get_setup_kwargs():
    """Builds a dictionary of kwargs for the setup function"""
    requirements = get_requirements()

    kwargs = dict(
        script_name="setup.py",
        name="SIMNet",
        version=__version__,
        author="PaiGramTeam",
        url="https://github.com/PaiGramTeam/SIMNet",
        keywords="genshin and honkai api wrapper",
        description="Modern API wrapper for Genshin Impact & Honkai: Star Rail built on asyncio and pydantic.",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=["tests*"]),
        install_requires=requirements,
        include_package_data=True,
        python_requires=">=3.8",
    )

    return kwargs


def main():  # skipcq: PY-D0003
    setup(**get_setup_kwargs())


if __name__ == "__main__":
    main()
