from django.urls import path
from .views import TriggerReportView

urlpatterns = [
    path('trigger_report', TriggerReportView.as_view()), ## to trigger a report
    path('trigger_report/<str:pk>/', TriggerReportView.as_view()) ## to download a triggered report
]
