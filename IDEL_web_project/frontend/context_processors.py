from .models import ImageFavicon, FooterBanner


def favicon_context(request):
    return {
        'favicon': ImageFavicon.objects.all().first(),
        'footer': FooterBanner.objects.all().first(),
    }
