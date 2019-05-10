import copy
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import TextStringObject, ByteStringObject


class PDFQuestionnaire(object):
    """
    Generic PDF parser that takes in a filepath to a fillable PDF form and
    return one dictionary object containing all fields in the form.

    TODO: add functions for validating that required fields has been filled

    """
    def __init__(self, fp):
        self.fp = fp
        self.process_file()

    def process_file(self):
        infile = PdfFileReader(open(self.fp, 'rb'))
        fields = infile.getFields()
        self.content = self.parse_fields(fields)

    def clean_comma_delim(self, v):
        if v is None:
            return []
        else:
            return [i.strip() for i in v.split(',') if i.strip()]

    def clean_fields(self, v):
        if type(v) is TextStringObject:
            v = str(v.strip())
            v = v.replace('\xa0', ' ')
        elif type(v) is ByteStringObject:
            v = v.decode('utf-8').strip().replace('\xa0', ' ')
            v = "\n\n".join([i for i in v.splitlines() if i.strip()])
        return v

    def parse_fields(self, fields):
        parsed_fields = {}
        for k,v in fields.items():
            cleaned_val = self.clean_fields(v.get('/V'))
            if '__' not in k:
                parsed_fields[k] = cleaned_val
                continue
            else:
                p, c = tuple(k.split('__'))

                if p in parsed_fields:
                    parsed_fields[p][c] = cleaned_val
                else:
                    parsed_fields[p] = {}
                    parsed_fields[p][c] = cleaned_val

        return parsed_fields


class ITSMetadataQuestionnaire(PDFQuestionnaire):
    """
    Parser for ITS DataHub Metadata Questionnaire that takes in a filepath to a
    fillable Metadata Questionnaire PDF and return one dictionary object containing
    all fields in the form in the format expected.

    """
    def __init__(self, fp):
        super().__init__(fp)

    def parse_fields(self, fields):
        parsed_fields = super().parse_fields(fields)
        distr = parsed_fields['distribution']
        parsed_fields['distribution'] = [distr]
        parsed_fields['bureauCode'] = ",".join(self.clean_comma_delim(parsed_fields['bureauCode']))
        parsed_fields['programCode'] = ",".join(self.clean_comma_delim(parsed_fields['programCode']))
        parsed_fields['keyword'] = self.clean_comma_delim(parsed_fields['keyword'])
        parsed_fields['trtTerms'] = self.clean_comma_delim(parsed_fields['trtTerms'])
        return parsed_fields

    def generate_dtg_metadata(self):
        q = self.content

        default_tags = ['intelligent transportation systems (its)','its joint program office (jpo)']
        default_attribution = 'U.S. Department of Transportation Intelligent Transportation Systems Joint Program Office (JPO)'
        default_category = 'Automobiles'
        default_contact_email = 'RDAE_Support@bah.com'

        commonCore = {
            'Contact Email': q['contactPoint']['hasEmail'],
            'Contact Name': q['contactPoint']['fn'],
            'Language': q['language'],
            'Update Frequency': q['accrualPeriodicity'],
            'License': 'Other',
            'Program Code': q['programCode'],
            'Bureau Code': q['bureauCode'],
            'Geographic Coverage': q['spatial'] or None,
            'Publisher': q['publisher']['name'],
            'Temporal Applicability': q['temporal'] or None,
            'Is Quality Data': 'True',
            'Public Access Level': q['accessLevel'].lower(),
            'Homepage': q['landingPage']
        }
        metadataUpsert = {
            'name': q['title'],
            'attribution': default_attribution,
            'description': q['description'],
            'privateMetadata': {'contactEmail': default_contact_email},
            'tags': list(set(q['keyword'] + default_tags)),
            'customFields': {'Common Core': commonCore},
            'category': default_category
        }
        return metadataUpsert

if __name__ == '__main__':
    """
    Quick test: python form_parsers.py
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fp = os.path.join(dir_path, '../forms/ITSJPO_MetadataQuestionnaire_fillable_v1.pdf')

    print('Parsing {}'.format(fp))
    mq = ITSMetadataQuestionnaire(fp)

    print('Content:')
    print(mq.content)