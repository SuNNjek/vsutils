from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vsutils",
    version="0.0.3",
    author="Sunner",
    author_email="sunnerlp@gmail.com",
    description="Some utilities to add some of the 'missing' functions that are in AVISynth but not Vapoursynth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuNNjek/vsutils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    "VapourSynth"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)