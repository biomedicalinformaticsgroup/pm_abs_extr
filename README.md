# pm_abs_extr

This repository automatically requests and extracts abstract from PubMed.

## Installation
pm_abs_extr has a number of dependencies on other Python packages, it is recommended to install it in an isolated environment.

`git clone https://github.com/biomedicalinformaticsgroup/pm_abs_extr.git`

`pip install ./pm_abs_extr`

## Get started

The only function available in this repository is called 'pubmed_abs_generation'. It only takes one argument 'PATH', which is the directory you want to save the output in. It has the default value './' meaning the current directory.

```python
from pm_abs_extr import pubmed_abs_generation
pubmed_abs_generation(PATH)
```

## The result

The function will generate a pre-made directory. Within ```$YOUR_PATH$/pubmed_abstract_output_YYYY```, you will find 2 subdirectories: 'xml_raw_files' and 'parsed_files'. In the xml_raw_files directory, it saves all the files requested from PubMed as a .gz format and their correponding unzip file. While in the 'parsed_files' directory we have one directory where the selected metadata are saved in the 'metadata' subdirectory and the abstracts are saved in the 'abstracts' subdirectory. 
The metadata files are composed of, when available:
- PMID: The PubMed Identifier associated with the publication.
- TITLE: Title of the publication.
- ABSTRACT_AVAILABLE: 1 if the abstract was found with the metadata 0 otherwise.
- DATE: What date the publication was released.
- LANGUAGE: The language used to write the publication.
- PUBLICATION_TYPE: The publication type.
- MESH: The MeSH terms associated with the publication.
- PUBMED_FILE: The PubMed file the information was extracted from.