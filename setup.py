import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vsutils",
    version="0.0.1",
    author="Sunner",
    author_email="sunnerlp@gmail.com",
    description="Some utilities to add some of the 'missing' functions that are in AVISynth but not Vapoursynth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuNNjek/vsutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)