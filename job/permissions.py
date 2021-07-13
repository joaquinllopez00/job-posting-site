from django.core.exceptions import PermissionDenied


def employer(function):

    def wrap(request, *args, **kwargs):

        if request.user.classification == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def employee(function):

    def wrap(request, *args, **kwargs):

        if request.user.classification == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
