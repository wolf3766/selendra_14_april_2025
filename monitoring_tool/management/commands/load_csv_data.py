import csv 
import os
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from monitoring_tool.models import Store, PollData, BusinessHours

class Command(BaseCommand):
    '''this file is being used to load csv files to database for further use'''
    
    def handle(self, *arg, **kwargs):
        store_status_file_path = os.path.join(settings.CSV_FILE_DIR, 'store_status.csv')
        store_timezone_file_path = os.path.join(settings.CSV_FILE_DIR, 'timezones.csv')
        store_menu_hours_file_path = os.path.join(settings.CSV_FILE_DIR, 'menu_hours.csv')
        store_map = {} ## is being used to store, store model objects in map, to get constant lookup
        
        with open(store_timezone_file_path, newline='') as store_timezone_csv:
            reader = csv.DictReader(store_timezone_csv)
            data = []
            for row in reader: ## store all the data to be created in an array 
                data.append(Store(store_id=row['store_id'], timezone_str=row['timezone_str']))
            Store.objects.bulk_create(data, ignore_conflicts=True) ## bulk insertion to reduce number of db calls 
            temp = Store.objects.all()
            for store in temp:
                store_map[store.store_id]=store       
        
        with open(store_status_file_path, newline='') as store_status_csv:
            reader = csv.DictReader(store_status_csv)
            data = []
            for row in reader:
                store_reference=store_map.get(row['store_id'])
                
                ## timestamp given in csv in not in correct format, formatting it and storing in db
                raw_timestamp = row['timestamp_utc']
                cleaned_timestamp = raw_timestamp.replace(" UTC", "").replace("“", "").replace("”", "").strip()
                parsed_timestamp = datetime.strptime(cleaned_timestamp, "%Y-%m-%d %H:%M:%S.%f")
                parsed_timestamp = parsed_timestamp.replace(tzinfo=timezone.utc)

                if store_reference is None:
                    continue
                
                ## store polldata in an array, later do bulk insertion at once.
                data.append(PollData( 
                    store = store_reference,
                    timestamp_utc=parsed_timestamp,
                    status=row['status']
                ))
            PollData.objects.bulk_create(data,ignore_conflicts=True)
        
        with open(store_menu_hours_file_path, newline='') as store_menu_hours_csv:
            reader = csv.DictReader(store_menu_hours_csv)
            data = []
            for row in reader:
                store_reference=store_map.get(row['store_id'])
                                
                if store_reference is None:
                    continue
                ## store business hours data in an array later, bulk insert at once.
                data.append(BusinessHours(
                    store = store_reference,
                    dayOfWeek = row['dayOfWeek'],
                    start_time_local = row['start_time_local'],
                    end_time_local = row['end_time_local']
                ))
            BusinessHours.objects.bulk_create(data, ignore_conflicts=True)
                
        self.stdout.write(self.style.SUCCESS("successfully loaded data from the csv")) 