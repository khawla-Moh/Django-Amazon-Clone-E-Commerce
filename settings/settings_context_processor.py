from .models import Settings



def get_settings(request):
    data=Settings.objects.last()
    return {'get_settings':data}