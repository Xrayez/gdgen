import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdgen",
    version="1.0a",
    author="Andrii Doroshenko (Xrayez)",
    author_email="xrayez@gmail.com",
    description="Code generator for Godot Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xrayez/gdgen",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            "gdgen = gdgen.cli:main"
        ]
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["wheel"],
    python_requires='>=3.6',
)
