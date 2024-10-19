# Settings context processor which should return the data like (logo, name of the webiste and contact us data and so on)
from django.core.cache import cache
from .models import Settings

def settings_data(request):
    data = cache.get('settings_data')
    if not data:
        data = Settings.objects.last()
        cache.set('settings_data', data, timeout=60 * 60 * 24 * 7) # for one week

    # print(data)
    return {'settings_data': data}
