from django.http import HttpResponseRedirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        common_errors = [403, 404, 500]
        if response.status_code in common_errors:
            return HttpResponseRedirect('/404')

        return response
