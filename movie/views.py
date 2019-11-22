from django.shortcuts import render
from django.contrib import messages
from airtable import Airtable
import os


AIRTABLE_API_KEY="key9KsVuPAMPNL2r1"
AIRTABLE_MOVIESTABLE_BASE_ID="appfmn1MGTBzGt8Ro"


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
              'Movie',
              api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))

# Create your views here.
