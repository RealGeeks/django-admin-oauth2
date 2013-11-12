from django.http import HttpResponse
from django.contrib.auth.models import User

def login(request):
    new_user = User(username='asdf', first_name='Kevin', last_name='McCarthy', email='asdf@asdf.com', is_staff=True, is_active=True, is_superuser=True)
    request.session['user'] = new_user
    return HttpResponse("ok, you're logged in")
