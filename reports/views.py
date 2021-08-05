from django.shortcuts import render
from django.http import JsonResponse
from profiles.models import Profile
# Create your views here.

def created_report_view(request):
    print(request.is_ajax)
    if request.is_ajax:
        name=request.POST.get('name')
        remarks=request.POST.get('remarks')
        image=request.POST.get('image')
        name=request.POST.get('name')

        # author=Profile.objects.get(user=request.user)
        return JsonResponse({"message":"send"})
    return JsonResponse({"message":"not ajax call"})




