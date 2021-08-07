from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from profiles.models import Profile
from django.template.loader import get_template
from .utils import get_report_image, link_callback
from .models import Report
from .forms import ReportForm
from xhtml2pdf import pisa
from datetime import datetime

# Create your views here.


class ReportListView(ListView):
    model=Report
    template_name="reports/report_list.html"
    context_object_name="report_list"

class ReportDetailView(DetailView):
    model=Report
    template_name="reports/report_detail.html"
    context_object_name="report"
    
class UploadTemplateView(TemplateView):
    template_name="reports/file_upload.html"

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


# def render_pdf_view(request,pk):
#     template_path = 'reports/pdf.html'
#     report=get_object_or_404(Report, pk=pk)
#     context ={
#         "report": report
#     }
#     # context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     #if download
#     # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     #if display
#     response['Content-Disposition'] = f'inline; filename="report_{datetime.now()}.pdf"'
    
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funy view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    report = get_object_or_404(Report, pk=pk)
    context = {'report': report}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def csv_upload_view(request):
    template_name="reports/file_upload.html"    

