from django.shortcuts import render
from django.http import JsonResponse
from profiles.models import Profile
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
# Create your views here.

def created_report_view(request):
    print(request.is_ajax)
    if request.is_ajax:
        form=ReportForm(request.POST or None)
        # name=request.POST.get('name')
        # remarks=request.POST.get('remarks')
        # image=request.POST.get('image')
        # name=request.POST.get('name')
        # author=Profile.objects.all().first()
        # Report.objects.create(name=name, image=img, remarks=remarks, auth=author)
        # author=Profile.objects.get(user=request.user)
        if form.is_valid:
            instance=form.save(commit=False)
            image=request.POST.get('image')
            img =get_report_image(image)
            instance.image=img
            instance.auth=Profile.objects.get(user=request.user)
            instance.save()
        return JsonResponse({"message":"send"})
    return JsonResponse({"message":"not ajax call"})




