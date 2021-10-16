# Import notre formulaire
from .forms import SearchForFriendForm

def search_form(request):
    form =  SearchForFriendForm()
    return {'search_form': form}