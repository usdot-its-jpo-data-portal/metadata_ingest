# coding=utf-8
import setuptools

setuptools.setup(
    name='metadata_ingest',
    version='0.0.13',
    author="Chueh Lien",
    author_email="lien_julia@bah.com",
    description="Package for parsing JPO's fillable Metadata Questionnaire PDF and for using parsed data to create a new dataset on Socrata (data.transportation.gov)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/usdot-its-jpo-data-portal/metadata_ingest",
    packages=['metadata_ingest'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests[security]>=2.20.0',
                      'PyPDF2>=1.26.0',
                      'socrata-py>=0.4.16']
)
