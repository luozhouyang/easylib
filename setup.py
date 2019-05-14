import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easylib",
    version="0.0.2",
    description="Frequently used functions and modules library for Python 3 by ZhouYang Luo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luozhouyang/easylib",
    author="ZhouYang Luo",
    author_email="zhouyang.luo@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[

    ],
    license="Apache License V2",
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
