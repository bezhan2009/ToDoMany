from django.http import JsonResponse


def ping(request):
    data = {'message': 'Servers is up and running'}
    return JsonResponse(data)
