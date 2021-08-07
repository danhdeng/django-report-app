from django.urls import path
from .views import (ReportListView, 
                    ReportDetailView, 
                    UploadTemplateView, 
                    render_pdf_view, 
                    created_report_view,
                    csv_upload_view)

app_name='reports'

urlpatterns=[
    path('save/',created_report_view, name="create-report"),
    path('upload/',csv_upload_view, name="upload"),
    path('<int:pk>/pdf/',render_pdf_view, name="report-generate"),
    path('',ReportListView.as_view(), name="report-list"),
    path('<int:pk>/',ReportDetailView.as_view(), name="report-detail"),
    path('from_file/',UploadTemplateView.as_view(), name="from-file"),
]