import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "SalesNexus"
AUTHOR_USER_NAME = "Phoenixarjun"
AUTHOR_EMAIL = "phoenixarjun007@gmail.com"

setuptools.setup(
    name=REPO_NAME,
    version=__version__,
    author="NARESH B A",
    author_email=AUTHOR_EMAIL,
    description="A Python package for SalesNexus, a sales prediction and analysis tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
)
