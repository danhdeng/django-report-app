from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .forms import ReportForm

# Create your views here.
@login_required
def created_report_view(request):
    form=ReportForm(request.POST or None)
    if request.is_ajax:
        # name=request.POST.get('name')
        # remarks=request.POST.get('remarks')
        # image=request.POST.get('image')
        # name=request.POST.get('name')

        # author=Profile.objects.get(user=request.user)
        if form.is_valid:
            form.save()
        return JsonResponse({"message":"send"})
    return JsonResponse({"message":"not ajax call"})




