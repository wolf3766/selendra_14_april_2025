from zoneinfo import ZoneInfo
from celery import shared_task
import os
from datetime import datetime, timedelta
import pandas as pd
from django.db.models import Max
from monitoring_tool.models import Store, BusinessHours, PollData, JobStore  
from monitoring_tool.services import calculate_uptime_downtime
from django.conf import settings
import pytz

@shared_task
def generate_report(report_id):
    # Step 1: Get all stores
    stores = Store.objects.values_list('store_id', 'timezone_str')
    # Step 2: Get max timestamp in production it should be current date-time 
    max_timestamp = PollData.objects.aggregate(Max('timestamp_utc'))['timestamp_utc__max']

    report_data = [] ## being used to store data calculated for csv file. 

    for store_id, timezone in stores:
        end_time = max_timestamp
        start_times = {
            'last_hour': end_time - timedelta(hours=1),
            'last_day': end_time - timedelta(days=1),
            'last_week': end_time - timedelta(weeks=1),
        }

        uptimes = {'last_hour': 0, 'last_day': 0, 'last_week': 0}
        downtimes = {'last_hour': 0, 'last_day': 0, 'last_week': 0}

        for period, start_time in start_times.items():
            business_hours = BusinessHours.objects.filter(
                store_id=store_id,
                start_time_local__lte=end_time.time(),
                end_time_local__gte=start_time.time()
            )

            polls = PollData.objects.filter(
                store_id=store_id,
                timestamp_utc__range=(start_time, end_time)
            ).order_by('timestamp_utc')

            ## add local time zone to business hours, before comparing it to UTC timezone, which is of polling data 
            for bh in business_hours:
                start_time_local = bh.start_time_local.replace(tzinfo=ZoneInfo(timezone))
                end_time_local = bh.end_time_local.replace(tzinfo=ZoneInfo(timezone))

                bh_start = (datetime.combine(end_time.date(), start_time_local)).astimezone(pytz.UTC)
                bh_end = (datetime.combine(end_time.date(), end_time_local)).astimezone(pytz.UTC)
                uptime, downtime = calculate_uptime_downtime(bh_start, bh_end, polls)
                uptimes[period] += uptime
                downtimes[period] += downtime

            ## data being returned is in minutes, to convert to hours please divide by  60
            ## in case of rounded values of hours use floor or //
        report_row = {
            "store_id": store_id,
            "uptime_last_hour": uptimes['last_hour'],
            "uptime_last_day": uptimes['last_day'] / 60,
            "uptime_last_week": uptimes['last_week'] / 60,
            "downtime_last_hour": downtimes['last_hour'],
            "downtime_last_day": downtimes['last_day'] / 60,
            "downtime_last_week": downtimes['last_week'] / 60,
        }
        report_data.append(report_row)

    # Step 3: Save report as CSV, in reports directory, with report_id name
    os.makedirs(os.path.join(settings.BASE_DIR, 'reports'), exist_ok=True)
    report_path = os.path.join(settings.BASE_DIR, 'reports', f'{report_id}.csv')
    pd.DataFrame(report_data).to_csv(report_path, index=False)

    # tasks[report_id] = 'Complete' 
    JobStore.objects.filter(job_id=report_id).update(status="completed")
    print(f"Report generated: {report_path}")
    
