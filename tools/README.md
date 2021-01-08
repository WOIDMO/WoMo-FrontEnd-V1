#How to run the the various data collectors

**US
  fetch_US_historic (this is only run once to initialize the historic data)

  weekly:
       1) fetch_US_recent.py
       2)process_US.py
      
**Europe
  fetch_EUROSTAT.py, process_EUROSTAT_historic.py, augment_historic_EUROSTAT.py
  
  weekly:
         1) fetch_EUROSTAT.py
         2) process_EUROSTAT_recent.py
         3) process_EUROSTAT_statistics.py
         
**Chile
  fetch_CL_historic.py
  
 weekly:
          1) fetch_CL_recent.py
          2) process_CL_statistics.py
