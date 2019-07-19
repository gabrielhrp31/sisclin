from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UpdateProfile
from django.contrib.auth.models import User


@login_required
def index(request):
    return redirect('schedule')


@login_required
def update_profile(request):
    form = UpdateProfile(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('my_profile')
    return render(request, 'dashboard/views/me/update_profile.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'dashboard/views/me/profile.html')


@login_required
def list_users(request):
    users = User.objects.all()
    return render(request, 'dashboard/views/users/list.html', {'users':users})


@staff_member_required
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        messages.success(request, messages.SUCCESS, "O usuário foi deletado")

    except User.DoesNotExist:
        messages.error(request, "O usuário não existe")
        return redirect('list_users')

    return redirect('list_users')
