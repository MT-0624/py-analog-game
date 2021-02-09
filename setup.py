import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygame",
    version="0.1.0",
    author="MT-0624",
    author_email="5191032@st.hsc.ac.jp",
    description="board game library in use!!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cm-hirano-shigetoshi/python_sample_command",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
