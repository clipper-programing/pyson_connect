from pathlib import Path
from setuptools import setup, find_packages

thisDir = Path(__file__).parent

setup(
        name="pyson_connect",
        version="0.2.4",
        author="Ryuse Sato(inchoxd)",
        author_email="incho@clpr.pro",
        description="pyson_connect: This is the third party module for using a Epson Connect",
        long_description = (thisDir/"README.md").read_text(),
        long_description_content_type = "text/markdown",
        url="https://github.com/clipper-programing/pyson_connect",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            ],
        install_requires=[
            "requests>=2.25.1",
            "Pillow>=8.0.1"
            ],
        python_requires=">=3.6",
        )
