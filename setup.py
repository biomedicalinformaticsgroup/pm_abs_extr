import setuptools
   
setuptools.setup(
    name="pm_abs_extr",
    version="0.1.0",
    author="Antoine Lain, Ian Simpson",
    author_email="Antoine.Lain@ed.ac.uk, Ian.Simpson@ed.ac.uk",
    description="This repository automatically requests and extracts abstract from PubMed.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
'bs4',
'wget',
'python-dateutil',
'IPython',
],
    python_requires='>=3.6'
)