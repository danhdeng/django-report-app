import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.template.loader import get_template
from django.utils.dateparse import parse_date
from .utils import get_report_image, link_callback
from .models import Report
from profiles.models import Profile
from products.models import Product
from customers.models import Customer
from sales.models import Sale, Position, CSV
from .forms import ReportForm
from xhtml2pdf import pisa
from datetime import datetime


# Create your views here.


class ReportListView(LoginRequiredMixin,ListView):
    model=Report
    template_name="reports/report_list.html"
    context_object_name="report_list"

class ReportDetailView(LoginRequiredMixin,DetailView):
    model=Report
    template_name="reports/report_detail.html"
    context_object_name="report"
    
class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name="reports/from_file.html"

@login_required
def created_report_view(request):
    if request.is_ajax:
        name=request.POST.get('name')
        remarks=request.POST.get('remarks')
        image=request.POST.get('image')
        img =get_report_image(image)
        author=Profile.objects.get(user=request.user)
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
@login_required
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

@login_required
def csv_upload_view(request):
    template_name="reports/file_upload.html"
    csv_file_name=request.FILES.get('file').name
    csv_file=request.FILES.get('file')
    obj, created =CSV.objects.get_or_create(file_name=csv_file_name)
    if created:
        obj.csv_file=csv_file
        obj.save()
        with open(obj.csv_file.path, 'r') as f:
            csv_read=csv.reader(f)
            csv_read.__next__()
            for row in csv_read:
                data="".join(row)
                data=data.split(';')
                data.pop()
                
                transaction_id=data[1]
                product=data[2]
                quantity=int(data[3])
                customer =data[4]
                date= datetime.combine(parse_date(data[5]), datetime.min.time())
                print(date)
                try:
                    product_obj=Product.objects.get(name__iexact=product)
                except Product.DoesNotExist:
                    product_obj = None
                print(product_obj)
                if product_obj is not None:
                    customer_obj, _ = Customer.objects.get_or_create(name=customer) 
                    salesman_obj = Profile.objects.get(user=request.user)
                    position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)
                    sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)
                    sale_obj.positions.add(position_obj)
                    sale_obj.save()
            return JsonResponse({"ex": False})   
    else:              
        return JsonResponse({"ex": True})   

