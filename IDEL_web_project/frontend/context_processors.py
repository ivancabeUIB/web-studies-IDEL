from .models import ImageFavicon, FooterBanner, HeaderImage


def favicon_context(requests):
    favicon = ImageFavicon.objects.all().first()
    footer = FooterBanner.objects.all().first()
    header_img = HeaderImage.objects.all().first()

    return {
        'favicon': favicon,
        'footer': footer,
        'header_img': header_img,
    }
