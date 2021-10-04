from codecs import open

from setuptools import find_packages, setup


with open("README.md", "r", encoding="UTF-8") as f:
    README = f.read()


EXTRAS = {
    "lint": ["black", "flake8", "isort"],
}
EXTRAS["dev"] = EXTRAS["lint"]


setup(
    name="testcase-maker",
    version="0.2.0.post1",
    author="benwoo1110",
    author_email="wben1110@gmail.com",
    description="Competitive programming testcases made easy!",
    extras_require=EXTRAS,
    install_requires=[
        "attrs~=21.2.0",
    ],
    license="MIT License",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/benwoo1110/testcase-maker",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
