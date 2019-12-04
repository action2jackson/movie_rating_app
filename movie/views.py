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
    # POST is for user input into backend
    if request.method == 'POST':
        # Dictionary
        data = {
            # Name that shows for movie when created
            'Name': request.POST.get('name'),
            # Picture needs a url to show
            'Pictures': [{'url': request.POST.get('url')}],
            # Rating that shows for movie when created int = only integers
            'Rating': int(request.POST.get('rating')),
            # Notes that show for movie when created
            'Notes': request.POST.get('notes')
        }
        # Adds data dictionary to Airtable server
        AT.insert(data)
    return redirect('/')


def edit(request, movie_id):
    # If the update button is hit by the user then ...
    if request.method == 'POST':
        # Copy and pasted this from the create function!
        data = {
            # Name that shows for movie when created
            'Name': request.POST.get('name'),
            # Picture needs a url to show
            'Pictures': [{'url': request.POST.get('url')}],
            # Rating that shows for movie when created int = only integers
            'Rating': int(request.POST.get('rating')),
            # Notes that show for movie when created
            'Notes': request.POST.get('notes')
        }
        # Each movie has an id, so the program takes in a specific id and ulters its data
        AT.update(movie_id, data)
    return redirect('/')

# Needs specific moviw to delete
def delete(request, movie_id):
    # Deletes the movie off of Airtable
    AT.delete(movie_id)
    return redirect('/')
