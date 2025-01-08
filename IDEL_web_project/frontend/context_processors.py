from .models import ImageFavicon, FooterBanner


def favicon_context(request):
    favicon = ImageFavicon.objects.all().first() if ImageFavicon.objects.all().exists() else ''
    footer = FooterBanner.objects.all().first() if FooterBanner.objects.all().exists() else []

    return {
        'favicon': favicon,
        'footer': footer,
    }
