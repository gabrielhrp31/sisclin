from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UpdateProfile


@login_required
def update_profile(request):
    form = UpdateProfile(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'dashboard/views/users/update_profile.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'dashboard/views/users/profile.html')

