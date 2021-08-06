from django.shortcuts import render
from django.http import JsonResponse
from profiles.models import Profile
from .utils import get_report_image
from .models import Report
# Create your views here.

def created_report_view(request):
    print(request.is_ajax)
    if request.is_ajax:
        name=request.POST.get('name')
        print(name)
        remarks=request.POST.get('remarks')
        image=request.POST.get('image')
        img=get_report_image(image)
        author=Profile.objects.all().first()
        Report.objects.create(name=name, image=img, remarks=remarks, auth=author)
        return JsonResponse({"message":"send"})
    return JsonResponse({"message":"not ajax call"})




