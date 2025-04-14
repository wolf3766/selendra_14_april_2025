1. fetch report. 

![image](https://github.com/user-attachments/assets/de0e61a8-74e0-49c4-b945-2b86fb5c9126)

2. trigger a report generation 

![image](https://github.com/user-attachments/assets/97f1c9ad-d12e-4a21-bdc6-c176515e0099)

3. report generated(also available as a file in repo)
https://drive.google.com/file/d/1VmEZFP_2ACnwpqjSb5NfwtxQS0R5jqR7/view?usp=sharing 

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
    4. we will fetch if the store was working in the current window of start and end time. that is hours/day/week
    5. we will convert the local business hours to UTC format, to compare with the polling data is working 
    6. we will fetch the polls with store_id in the current window
    7. after that we will iterate over the polling data,to fetch the number if minutes our restaurant was active/inactive
    8. at last we will store all calculated data in an array.
    9. from the array we can create a csv file to store our data.
  
3. Logic to load the huge data available in our csv.
     1. we will create objects of your models(Store,businessHours,JobStore)
     2. when an entry is being fetched from the csv we will create above object and store in the array
     3. at the end of the csv we will have all the data, that can be pushed using Bulkcreate.

4. Some assumptions that i have taken
    1. since my whole logic is based on store Table, so all the entries in tables such as BusinessHours and PollData as directly dependent on Store data
    2. if a store do not exist but its poll-data/business-hours exist in that case i have simply discarded those values as store value is important.
    3. this is being used to streamline the data.
    4. another way could have been, if i found business-hours without store, then creating a new store with that id, but that approach is not feasible, as this might lead to redudent entries.
