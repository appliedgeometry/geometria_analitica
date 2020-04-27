from django.shortcuts import render


# Define error templates
def bad_request(request, exception=None):
    response = render(request, 'errors/400.html')
    response.status_code = 400
    return response


def permission_denied(request, exception=None):
    response = render(request, 'errors/403.html')
    response.status_code = 403
    return response


def page_not_found(request, exception=None):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def server_error(request, exception=None):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return response
