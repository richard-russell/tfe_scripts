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
