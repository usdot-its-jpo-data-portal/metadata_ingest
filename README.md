# metadata-ingest
Utilities for parsing ITS DataHub Metadata Questionnaire and ingesting metadata of data sets to ITS DataHub.

# Quick Start
1. Clone this GitHub repository.
2. Install required Python packages with `pip install -r requirements.txt`
3. Update the `metadata_ingest/const.py` file with your credentials, OR, copy the CONFIG SECTION of the `const.py` file to create `metadata_ingest/const_local.py` and update the `const_local.py` file with your Socrata credentials
4. Run `python metadata_ingest/socrata_ingestor.py` to test creating a dataset in the Socrata platform of your choice, using the metadata information from the sample Metadata Questionnaire at `forms/ITSJPO_MetadataQuestionnaire_fillable_v1_sample.pdf`
