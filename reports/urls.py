from django.urls import path
from .views import created_report_view, ReportListView, ReportDetailView, generated_report_view

app_name='reports'

urlpatterns=[
    path('save/',created_report_view, name="create-report"),
    path('',ReportListView.as_view(), name="report-list"),
    path('<int:pk>/',ReportDetailView.as_view(), name="report-detail"),
    path('<int:pk>/generate',generated_report_view, name="report-generate"),


]