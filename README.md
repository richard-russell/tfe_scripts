# TFE Scripts
Python scripts for extracting run data from TFE/TFC via API.

## Workspace Run Times
Prints a list of the last runs (up to 100), the time and date created and the elapsed time
of the plan, in CSV format. 

Run as follows:
```
> python wsplantimes.py
```
Prompts for the following values, which can also be supplied as environment variables:
```
TFE_URL
TFE_ORG
TFE_WORKSPACE
TFE_TOKEN
```

## Workspace Resource Counts
Prints a list of all workspaces in the specified org, and the count of resources. 

Run as follows:
```
> python wsresources.py
```
Prompts for the following values, which can also be supplied as environment variables:
```
TFE_URL
TFE_ORG
TFE_TOKEN
```

## What Ran When
Prints a list of all runs created in the specified time window in the specified org. 

Run as follows:
```
> python whatranwhen.py STARTTIME ENDTIME
```
Where STARTTIME and ENDTIME are in the format `YYYY-MM-DDTHH:MM:SS`.

For example: `python whatranwhen.py 2023-04-01T09:00:00 2023-05-01T09:00:00`

Note: this script uses simple lexical comparison of dates to work out if the timestamp is in the specified window. This is for speed, and to avoid using the datetime module which can cause problems on some hosts. It relies on each successive character in the datetime string being less significant than the previous. If your timestamps are in a different format, this script will give unpredicatable results.

Prompts for the following values, which can also be supplied as environment variables:
```
TFE_URL
TFE_ORG
TFE_TOKEN
```
