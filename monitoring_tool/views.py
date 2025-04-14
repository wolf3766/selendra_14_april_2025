import os
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from monitoring_tool.models import JobStore
from rest_framework import status
from .generate_report_task import generate_report
import uuid
import pdb

# Create your views here.
class TriggerReportView(APIView):
    def post(self, request):
        report_id = str(uuid.uuid4())
        JobStore.objects.create(job_id=report_id, status="running")
        generate_report.delay(report_id)
        # pdb.set_trace()

        return Response(data={
                                "report_id": report_id, 
                                "message": "please wait report is being generated"
                            }, status=status.HTTP_200_OK)
    
    def get(self, request, pk):
        try:
            job = JobStore.objects.get(job_id=pk)
        except JobStore.DoesNotExist:
            return Response(data={"message": "Report with the provided ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if job.status == "running":
            return Response(status=status.HTTP_302_FOUND, data={"job_id": pk,"message":"this job is still prcoessing"})
        
        file_path = f'reports/{pk}.csv'
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'report_{pk}.csv')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data="report with this passed id have been moved")
        