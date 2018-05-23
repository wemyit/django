from django.conf import settings


def google_analytics(request):
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)
    if not settings.DEBUG and ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_prop_id,
        }
    return {}
