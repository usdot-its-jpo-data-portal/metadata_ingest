# metadata-ingest
Utilities for parsing ITS DataHub Metadata Questionnaire and ingesting metadata of datasets to ITS DataHub.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for use, development, and testing purposes.

### Prerequisites

1. Have access to Python 3.6+. You can check your python version by entering `python --version` and `python3 --version` in command line.
2. Have access to the command line of a machine. If you're using a Mac, the command line can be accessed via the [Terminal](https://support.apple.com/guide/terminal/welcome/mac), which comes with Mac OS. If you're using a PC, the command line can be accessed via the Command Prompt, which comes with Windows, or via [Cygwin64](https://www.cygwin.com/), a suite of open source tools that allow you to run something similar to Linux on Windows.

### Installation

1. Download the script by cloning the module's [code repository on GitHub](https://github.com/usdot-its-jpo-data-portal/metadata_ingest). You can do so by running one of the following in command line. If unfamiliar with how to clone a repository, follow the [official GitHub guide](https://help.github.com/en/articles/cloning-a-repository).
    - via HTTP: `git clone https://github.com/usdot-its-jpo-data-portal/metadata_ingest.git`
    - via SSH (if using 2-factor authentication): `git clone git@github.com:usdot-its-jpo-data-portal/metadata_ingest.git`
2. Navigate into the repository folder by entering `cd metadata_ingest` in command line.
3. Run `pip install -e .` to install the metadata_ingest Python package.
4. Install the required packages by running `pip install -r requirements.txt`.
5. Update the `metadata_ingest/const.py` file with your credentials, OR, copy the CONFIG SECTION of the `const.py` file to create `metadata_ingest/const_local.py` and update the `const_local.py` file with your Socrata credentials

### Testing

Run `python metadata_ingest/form_parsers.py` to test parsing the sample [metadata questionnaire](metadata_ingest/forms/ITSJPO_MetadataQuestionnaire_fillable_sample.pdf) included in the `forms` folder of this repository. The parsed information will be shown in the command line interface.

Run `python metadata_ingest/socrata_ingestor.py` to test creating a dataset in the Socrata platform of your choice, using the metadata information from the sample Metadata Questionnaire at `forms/ITSJPO_MetadataQuestionnaire_fillable_sample.pdf`

### Usage

#### Use as python package
The form parsers and Socrata dataset creator can be imported into your own code by adding the following statement:

`from metadata_ingest.form_parsers import ITSMetadataQuestionnaire, PDFQuestionnaire`
`from metadata_ingest.socrata_ingestor import SocrataDataset`

Sample usage have been provided in the [demo.ipynb](demo.ipynb) file in this repository.

## Built With

* [Python 3.6+](https://www.python.org/download/releases/3.0)
* [PyPDF2](http://mstamy2.github.io/PyPDF2/): Python package used to parse the fillable PDF.
* [socrata-py](https://github.com/socrata/socrata-py): Python SDK for the Socrata Data Management API.
* [requests](https://requests.readthedocs.io/en/master/): elegant and simple HTTP library for Python.

## Contributing

1. [Fork it](https://github.com/usdot-its-jpo-data-portal/metadata_ingest/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for general good practices on code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the Apache 2.0 License. - see the [LICENSE](LICENSE) file for details

## Release History
* 0.1.0
  * Initial version

## Known Bugs
*

## Contact information
ITS DataHub Team: data.itsjpo@dot.gov
Distributed under Apache 2.0 License. See *LICENSE* for more information.

## Credits and Acknowledgment
Thank you to the Department of Transportation for funding to develop this project.

## CODE.GOV Registration Info
* __Agency:__ DOT
* __Short Description:__ Python package for parsing ITS DataHub Metadata Questionnaire and ingesting metadata of datasets to the U.S. DOT's Socrata platform (data.transportation.gov).
* __Status:__ Beta
* __Tags:__ transportation, fillable PDF, intelligent transportation systems, python, ITS DataHub
* __Labor Hours:__ 0
* __Contact Name:__ Brian Brotsos
* __Contact Phone:__ 202-366-9013
