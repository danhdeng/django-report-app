from django.urls import path
from .views import created_report_view

app_name='reports'

urlpatterns=[
    path('save/',created_report_view, name="create-report")
]