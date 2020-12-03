from django.shortcuts import render, redirect

def adult_or_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated or "age" in request.session:
            if request.session.get('age') > 17:
                return func(request)
            else:
                return redirect('underage')
        else:
            return redirect('checkage')
    return wrapper
