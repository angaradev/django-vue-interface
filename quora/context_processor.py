from django.conf import settings

def main_host(request):
    """
    Here I defined main site url to use it in vue.js file
    """
    scheme = request.is_secure() and "https" or "http"
    host = request.get_host()
    return {'MAIN_HOST': f"{scheme}://{host}"}
