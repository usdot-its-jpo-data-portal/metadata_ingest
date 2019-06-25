import copy
from itertools import groupby
import json
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

    def preparse_contactPoints(self, fields):
        key = lambda x: x[0]
        contactPointFields = set([k for k in fields if 'contactPoint' in k])
        roleFieldValTuples = [(*k.split('__')[1:], v['/V']) for k, v in fields.items() if k in contactPointFields]
        contactFieldGroups = groupby(sorted(roleFieldValTuples, key=key), key=key)
        contactPoint = [{'hasRole':k,
                        **{f:v for r,f,v in list(g)}}
                         for k,g in contactFieldGroups]
        for k in contactPointFields:
            del fields[k]
        return fields, contactPoint

    def parse_identifiersExtended(self, identifiersExtended):
        identifiersExtended = [dict(zip(['type', 'uid'], entry.split(':')))
                                 for entry in identifiersExtended.split(',')]
        for idx, entry in enumerate(identifiersExtended):
            identifiersExtended[idx]['type'] = identifiersExtended[idx]['type'].lower().strip()
            identifiersExtended[idx]['uid'] = identifiersExtended[idx]['uid'].lower().strip()
        return identifiersExtended

    def parse_fields(self, fields):
        fieldsMod, contactPoint = self.preparse_contactPoints(fields)
        parsed_fields = super().parse_fields(fieldsMod)
        distr = parsed_fields['distribution']
        parsed_fields['distribution'] = [distr]
        parsed_fields['bureauCode'] = ",".join(self.clean_comma_delim(parsed_fields['bureauCode']))
        parsed_fields['programCode'] = ",".join(self.clean_comma_delim(parsed_fields['programCode']))
        parsed_fields['keyword'] = self.clean_comma_delim(parsed_fields['keyword'])
        parsed_fields['identifiersExtended'] = self.parse_identifiersExtended(parsed_fields['identifiersExtended'])
        parsed_fields['contactPoint'] = contactPoint
        return parsed_fields

    def generate_dtg_metadata(self):
        q = self.content

        default_tags = ['intelligent transportation systems (its)','its joint program office (jpo)']
        default_attribution = 'U.S. Department of Transportation Intelligent Transportation Systems Joint Program Office (JPO)'
        default_category = 'Automobiles'
        default_contact_email = 'RDAE_Support@bah.com'

        contactPoint_dataSteward = [i for i in q['contactPoint'] if i['hasRole'] == 'dataSteward'][0]

        commonCore = {
            'Contact Email': contactPoint_dataSteward['hasEmail'],
            'Contact Name': contactPoint_dataSteward['fn'],
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
    fp = os.path.join(dir_path, '../forms/ITSJPO_MetadataQuestionnaire_fillable_v2_sample.pdf')

    print('Parsing {}'.format(fp))
    mq = ITSMetadataQuestionnaire(fp)

    print('Content:')
    print(json.dumps(mq.content,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')))
