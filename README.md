# WoMo-FrontEnd-V1

WoMo Front-End v1 World-wide mortality monitoring system (Python/Dash) 

The live application can be viewed at: https://www.woidmo.org/home/womo/


**How this works

Excess mortality data avoid miscounting deaths from the under-reporting of Covid-19-related deaths and other health conditions left untreated. Excess mortality is defined as actual deaths from all causes, minus ‘normal’ deaths (historic mortality data). 
For historic mortality data, we exclude the year 2020 and 2021 will also be excluded in the future, since these are years with abnormal mortality. In general, pandemic years are always excluded.

**Practical

The front-end is a Dash app with routes for every region
The app is hosted on Heroku

The tools directory contains the python scripts to collect and process the data. These are run once per week. (Check the readme in the dir for running order)
The data directory contains all of the data. There are two files with historic data that need to be unzipped.

**Contributing

Anyone can contribute to this project. We welcome others to join and make it better.
Code refactoring and making minor improvements do not need to be discussed.
For changing functionality and other major changes, it's best to reach out first. Contact us at volunteer@woidmo.org
