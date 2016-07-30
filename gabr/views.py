from django.shortcuts import render


def handle_404(request):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handle_500(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response
