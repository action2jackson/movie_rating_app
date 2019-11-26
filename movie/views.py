from django.shortcuts import render, redirect
from django.contrib import messages
# Need this import for airtable to connect
from airtable import Airtable
import os


AIRTABLE_API_KEY="key9KsVuPAMPNL2r1"
AIRTABLE_MOVIESTABLE_BASE_ID="appfmn1MGTBzGt8Ro"


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
              # The name of the airtable table you will be referring to
              'Movie',
              # Getting the api key
              api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))

# Create your views here.
def home_page(request):
    # Finds what the user inputs and fills in an empty string that equals query
    user_query = str(request.GET.get('query', ''))
    # Gets users input, puts it in lower case and then finds it smartly
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    # makes search_result callable for front-end
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movie/movie_stuff.html', stuff_for_frontend)

def create(request):
    return redirect('/')
