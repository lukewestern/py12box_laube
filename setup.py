import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py12box_laube",
    version="0.0.1",
    author="Luke Western",
    author_email="luke.western@bristol.ac.uk",
    description="AGAGE 12-box model for UEA/FZJ data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
