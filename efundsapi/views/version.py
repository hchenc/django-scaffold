from django.http import JsonResponse

from efunds import version


def get_version(request) -> JsonResponse:
    return JsonResponse({'version': version.VERSION})
