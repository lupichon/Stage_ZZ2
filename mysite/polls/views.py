from django.http import HttpResponse
from django.views import View


def my_custom_view(request):
    return HttpResponse("Bienvenue sur ma vue personnalisée !")
