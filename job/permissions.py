from django.core.exceptions import PermissionDenied


def employer(function):

    def wrap(request, *args, **kwargs):

        if request.user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def employee(function):

    def wrap(request, *args, **kwargs):

        if request.user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
