from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(views_func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return views_func(request, *args, **kwargs)
    return inner


def allowed_users(allowed_roles=[]):
    def outer(views_func):
        def inner(request, *args, **kwargs):
            user_group = None
            if request.user.groups.exists():
                all_groups = request.user.groups.all()
                user_group = all_groups[0].name

            if user_group in allowed_roles:
                return views_func(request, *args, **kwargs)
            else:
                return HttpResponse('Sorry! You are not allowed to see this page.')
        return inner
    return outer


def admin_only(views_func):
    def inner(request, *args, **kwargs):
         user_group = None
         if request.user.groups.exists():
             all_groups = request.user.groups.all()
             user_group = all_groups[0].name

         if user_group == 'admin':
             return views_func(request, *args, **kwargs)
         elif user_group == 'customer':
             return redirect('user_page')
         else:
             return HttpResponse('Sorry! You are not allowed to see this page')
    return inner
             







