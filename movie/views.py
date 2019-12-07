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
            # If there is no url for the picture input then show this image by default
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png'}],
            # Rating that shows for movie when created int = only integers
            'Rating': int(request.POST.get('rating')),
            # Notes that show for movie when created
            'Notes': request.POST.get('notes')
        }
        # Error checking
        try:
            # Adds data dictionary to Airtable server
            response = AT.insert(data)
            # when movie is created it gets its name through the Airtable field and then shows it in an alert message
            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            # checks that all the formatting is correct and if it isnt throws up a warning bar
            # format(e) when formatting is off it call e, which is Exception
            messages.warning(request, 'Got an error when trying to create new movie: {}'.format(e))
    return redirect('/')


def edit(request, movie_id):
    # If the update button is hit by the user then ...
    if request.method == 'POST':
        # Copy and pasted this from the create function!
        data = {
            # Name that shows for movie when created
            'Name': request.POST.get('name'),
            # Picture needs a url to show
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png'}],
            # Rating that shows for movie when created int = only integers
            'Rating': int(request.POST.get('rating')),
            # Notes that show for movie when created
            'Notes': request.POST.get('notes')
        }
        try:
            # Each movie has an id, so the program takes in a specific id and ulters its data
            response = AT.update(movie_id, data)
            # same message alert as create movie except this for editing a movie
            # success makes the alert message look green
            messages.success(request, 'successfully updated movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to update a movie: {}'.format(e))
    return redirect('/')

# Needs specific moviw to delete
def delete(request, movie_id):
    try:
        # gets the movie id, gos into its fields and gets the name of the movie
        # needed to get this movies name right from airtable because its getting deleted completely out of the database
        movie_name = AT.get(movie_id)['fields'].get('Name')
        # Deletes the movie off of Airtable
        AT.delete(movie_id)
        # calls the movie_name variable
        # warning makes the alert message look red
        messages.warning(request, 'Deleted movie:{}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'There was an error when trying to delete a movie: {}'.format(e))
    return redirect('/')
