from setuptools import setup, find_packages

setup(
    name="crystal_laser_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # No dependencies beyond standard library
    ],
    author="Madan Kumar Shankar",
    author_email="madan.mx@gmail.com",
    description="Tools for calculating chromophore concentrations and laser-sample interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/madanmx/crystal-laser-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "crystal-laser-tools=crystal_laser_tools.cli:main_menu",
        ],
    },
)
