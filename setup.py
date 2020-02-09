import setuptools


setuptools.setup(
    name="machine-learning",
    version="0.0.1",
    author="Maxwell Flitton",
    author_email="maxwellflitton@gmail.com",
    description="web scraping",
    long_description="basic library for web scraping",
    long_description_content_type="text/markdown",
    url="https://github.com/MonolithAILtd/machine-learning.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Build Tools"
    ),
    install_requires=[
        "requests",
        "bs4"
    ],
    zip_safe=False
)
