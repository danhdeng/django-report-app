from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from profiles.models import Profile
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
# Create your views here.


class ReportListView(ListView):
    model=Report
    template_name="reports/report_list.html"
    context_object_name="report_list"

class ReportDetailView(DetailView):
    model=Report
    template_name="reports/report_detail.html"
    context_object_name="report"

def created_report_view(request):
    print(request.is_ajax)
    if request.is_ajax:
        name=request.POST.get('name')
        remarks=request.POST.get('remarks')
        image=request.POST.get('image')
        img =get_report_image(image)
        author=Profile.objects.all().first()
        Report.objects.create(name=name, image=img, remarks=remarks, auth=author)
        
        # form=ReportForm(request.POST or None)
        # if form.is_valid:
        #     instance=form.save(commit=False)
        #     image=request.POST.get('image')
        #     img =get_report_image(image)
        #     instance.image=img
        #     instance.auth=Profile.objects.get(user=request.user)
        #     instance.save()
        return JsonResponse({"message":"send"})
    return JsonResponse({"message":"not ajax call"})


def generated_report_view(request, **kwargs):
    print("generate the pdf for report")
    return JsonResponse({"message":"generate the pdf for report"})



