# Settings context processor which should return the data like (logo, name of the webiste and contact us data and so on)

from .models import Settings

def settings_data(request):
    settings_data = Settings.objects.last()

    return {'settings_data': settings_data}
