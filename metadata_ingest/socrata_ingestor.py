import json
import os
import requests
from socrata.authorization import Authorization
from socrata import Socrata

import const
from form_parsers import ITSMetadataQuestionnaire


auth_param = (
  const.SOCRATA_DOMAIN,
  const.SOCRATA_USERNAME,
  const.SOCRATA_PASSWORD
)

class SocrataDataset(object):
    def __init__(self, uuid=None, mq_fp=None, auth_param=auth_param):
        self.existing_dataset = bool(uuid)
        self.uuid = uuid
        self.mq_fp = mq_fp
        self.auth_param = auth_param
        self.socrata = Socrata(Authorization(*auth_param))
        self.mq = None
        self.metadata = None

        if mq_fp:
            self.mq = ITSMetadataQuestionnaire(mq_fp)
        self.retrieve_metadata()

    def generate_dataset_url(self):
        return 'https://{}/d/{}'.format(self.auth_param[0], self.uuid)

    def retrieve_metadata(self):
        if self.uuid:
            url = 'https://{}/api/views/metadata/v1/{}'.format(self.auth_param[0], self.uuid)
            r = requests.get(url, auth=self.auth_param[1:])
            self.metadata = r.json()
        return

    def create_dataset(self):
        if self.uuid is None:

            # NOTE: publishing this way seems to default to creating integrated data set only
            # TODO: modify so that we can publish external datasets
            # TODO: fix permission - right now it's published as public data set

            revision_json = self.mq.generate_dtg_metadata()
            revision_json.update({'action': {'type': 'update', 'permission': 'private'}})

            (ok, revision) = self.socrata.new(revision_json)
            (ok, job) = revision.apply()
            (ok, job) = job.wait_for_finish(progress=lambda job: print('Job progress:', job.attributes['status']))
            self.uuid = revision.view_id()
            print('Dataset has been created at {}'.format(self.generate_dataset_url()))
        else:
            print('Dataset already exists at {}'.format(self.generate_dataset_url()))
        return

    def update_metadata(self):
        if self.uuid:
            url = 'https://{}/api/views/metadata/v1/{}'.format(self.auth_param[0], self.uuid)
            response = requests.patch(url,
                              auth=self.auth_param[1:],
                              data=json.dumps(self.mq.generate_dtg_metadata()))
            if response.status_code != 200:
                print(response)
            else:
                print('Metadata updated for {}'.format(self.generate_dataset_url()))


if __name__ == '__main__':
    """
    Quick test: python socrata_ingestor.py

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pdf_fp = os.path.join(dir_path, '../forms/ITSJPO_MetadataQuestionnaire_fillable_v1_sample.pdf')
    # pdf_file_name_test = '/Users/julialien/Desktop/its_deployment_lessons_attachments/ITS_benefits_database_in_ITS_datahub/ITSJPO_MetadataQuestionnaire_fillable_v1_BenefitsTest.pdf'
    dataset = SocrataDataset(uuid=None, mq_fp=pdf_fp)

    dataset.create_dataset()
    dataset.update_metadata()
