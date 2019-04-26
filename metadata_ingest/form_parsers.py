import copy
from PyPDF2 import PdfFileWriter, PdfFileReader



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

    @classmethod
    def clean_comma_delim(self, v):
        if v is None:
            return []
        else:
            return [i.strip() for i in v.split(',') if i.strip()]

    def parse_fields(self, fields):
        parsed_fields = {}
        for k,v in fields.items():
            if '__' not in k:
                parsed_fields[k] = v.get('/V') or None
                continue
            else:
                p, c = tuple(k.split('__'))

                if p in parsed_fields:
                    parsed_fields[p][c] = v.get('/V') or None
                else:
                    parsed_fields[p] = {}
                    parsed_fields[p][c] = v.get('/V') or None

        return parsed_fields


class ITSMetadataQuestionnaire(PDFQuestionnaireParser):
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
        parsed_fields['bureauCode'] = self.clean_comma_delim(parsed_fields['bureauCode'])
        parsed_fields['programCode'] = self.clean_comma_delim(parsed_fields['programCode'])
        return parsed_fields

if __name__ == '__main__':
    """
    Quick test: python form_parsers.py
    """
    fp = '../forms/ITSJPO_MetadataQuestionnaire_fillable_v1.pdf'

    print('Parsing {}'.format(fp))
    mq = ITSMetadataQuestionnaire(fp)

    print('Content:')
    print(mq.content)
