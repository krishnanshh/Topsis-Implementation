from setuptools import setup, find_packages

setup(
    name="topsis-Krishnansh_Verma_102203103",
    version="1.0.0",
    author="Krishnansh Verma",
    description="This Python package implements the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method for rank calculation. It helps in ranking alternatives based on multiple criteria by determining their proximity to the ideal and negative-ideal solutions. The package is efficient and easy to use for decision-making tasks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    packages=find_packages(),  
    install_requires=[
        "numpy",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis.102203103:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
