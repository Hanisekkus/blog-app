from django.conf import settings

def cache(request):
    return {'CACHE_TIMEOUT': settings.CACHES['default']['TIMEOUT']}
