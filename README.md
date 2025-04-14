1. fetch report. 

![image](https://github.com/user-attachments/assets/de0e61a8-74e0-49c4-b945-2b86fb5c9126)

2. trigger a report generation 

![image](https://github.com/user-attachments/assets/97f1c9ad-d12e-4a21-bdc6-c176515e0099)

3. report generated(also available as a file in repo)
https://drive.google.com/file/d/1VmEZFP_2ACnwpqjSb5NfwtxQS0R5jqR7/view?usp=sharing

5. How to Run the application?
    1. python manage.py makemigrations // used to create migrations 
    2. python manage.py migrate // to run the migrations 
    3. python manage.py runserver // to run the server
    4. python manage.py load_csv_data // to load csv files in database
    5. celery -A loop_assignment worker --loglevel=info // in a different terminal, used to run a worker process, which will work in async manner 

6. Overlapping intervals logic explanation: 
lets say our the range in which we are calculating uptime downtime is form 10am to 12pm, now an overlapping interval will be something from 9am to 1pm,
now i have defined query, as such start_time_range<=end_time_interval.time() && end_time_range>=start_time_interval.time() then we consider that range, 
so in our case, 10am(range start time) is smaller then 12pm(interval end time) and 12pm( range end-time) greater then 9am interval start-time 

7. how generating report is being handled?
    1. generating report is being handled in async manner, cause generating report is taking around 25-30 seconds
    2. we have a used a background job scheduler, **celery** with a worker to execute these tasks as soon as they arrive.
    3. a shared task is being used to generate and save csv files in our local system. 

Code explanation: 
1. Tables used?
    1. store (to store data from store csv file)
    2. businessHours (to store each store working hours)
    3. PollData (to store when each store was polled)
    4. job_store (to store job trigger of reports)

2. Logic to fetch uptime and downtime for each store. 
    1. we will fetch the last recorded time from our polling data and mark this as end time, in  production this should be current time
    2. we will calculate the start time, based on end time, that is 1hours,1 day, 1 week before
    3. we will fetch all the stores that are registered in our database
    4. we will create time windows, for hour,week,day based on above fetched end_time and start_time 
    5. inside each window, we fetch the business hours and polling data 
    6. we will convert the local business hours to UTC format, to compare with the polling data
    7. we will fetch the polls with store_id in the current window
    8. after that we will iterate over the polling data,to fetch the number of minutes our restaurant was active/inactive
    9. at last we will store all calculated data in an array.
    10. from the array we can create a csv file to store our data.
  
3. Logic to load the huge data available in our csv.
     1. we will create objects of your models(Store,businessHours,JobStore)
     2. when an entry is being fetched from the csv we will create above object and store in the array
     3. at the end of the csv we will have all the data, that can be pushed using Bulkcreate.

4. Some assumptions that i have taken
    1. since my whole logic is based on store Table, so all the entries in tables such as BusinessHours and PollData as directly dependent on Store data
    2. if a store do not exist but its poll-data/business-hours exist in that case i have simply discarded those values as store value is important.
    3. this is being used to streamline the data.
    4. another way could have been, if i found business-hours without store, then creating a new store with that id, but that approach is not feasible, as this might lead to redudent entries.

5. what can be improved?
   1. instead of running based on csv file last date, we should use current date-time, to get latest report
   2. can move the csv file to cloud such as s3, for backup and fault tolerance
   3. can use queue model with celery such that each worker only listens for tasks in a particular queue.
   4. can manage the theards that are being used by a worker. for fast processing and concurrency of tasks
   5. can add cron job/database trigger to automatically load csv files to database.
