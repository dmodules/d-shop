from django.http import JsonResponse, HttpResponse

from .models import ThemeManagement


def get_css(request):

    theme = request.GET.get('theme', '')

    #Search for active theme
    if theme:
        theme = ThemeManagement.objects.filter(theme=theme).first()
    else:
        theme = ThemeManagement.objects.filter(active=True).first()

    if theme:
        return HttpResponse(theme.css)
    return JsonResponse({})
