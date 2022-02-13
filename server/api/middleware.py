import json
from .models.user import User
from django.conf import settings


def check_accesses(get_response):
    def middleware(request):
        path = request.path.replace('/', '')
        if path in settings.CHECK_URL_FOR_SUPERUSER_ACCESS and request.method == 'POST':
            data = json.loads(request.body)
            if 'owner_wallet_address' in data:
                user = User.objects.filter(wallet=str(data['owner_wallet_address']))

                if user:
                    return get_response(request)
                else:
                    raise Exception('Access denied!')
            else:
                raise Exception('Access denied!')

        return get_response(request)

    def process_exception(request, exception):
        # Do something useful with the exception
        pass

    middleware.process_exception = process_exception
    return middleware
