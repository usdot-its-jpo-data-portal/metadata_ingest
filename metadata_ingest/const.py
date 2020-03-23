"""
Modify the config section below, OR copy the CONFIG SECTION to a new file in
this folder called "const_local.py".
"""

import os

### CONFIG SECTION STARTS ###

SOCRATA_DOMAIN = 'data.transportation.gov'
SOCRATA_USERNAME = None
SOCRATA_PASSWORD = None
SOCRATA_API_KEY = None

### CONFIG SECTION ENDS ###

# check for local const file
dir_path = os.path.dirname(os.path.realpath(__file__))
local_const_path = os.path.join(dir_path, 'const_local.py')
if SOCRATA_USERNAME is None and os.path.exists(local_const_path):
    from metadata_ingest.const_local import *
