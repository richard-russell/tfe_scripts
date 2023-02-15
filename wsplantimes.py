# Retrieve time created and plan duration for last X runs in a specified TFE/TFC workspace
# NB: skeleton code ... only checks for basic errors in responses
# Reads inputs from env vars or interactively

import datetime
from getpass import getpass
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

VERIFY = True  # verify API cert by default. Change to False to force less secure behaviour.
PAGESIZE = 100
TS_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

if VERIFY == False:
    print('Certificate verification disabled. Use at your own risk!')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def envorask(var, sensitive=False):
    """Retrieve environment variable called 'var', and if it
       doesn't exist, prompt for it via interactive input,
       optionally using getpass if secure=True
    """
    value = os.getenv(var)
    if value is not None:
        return value
    if sensitive:
        return getpass(f'{var}: ')
    return input(f'{var}: ')

# These variables are populated from environment variables if they exist, else prompt for input
TFE_URL = envorask('TFE_URL')
TFE_ORG = envorask('TFE_ORG')
TFE_WORKSPACE = envorask('TFE_WORKSPACE')
TFE_TOKEN = envorask('TFE_TOKEN', sensitive=True)

headers = { "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {TFE_TOKEN}"}

# Find workspace details, primarily id
r_ws = requests.get(f"{TFE_URL}/api/v2/organizations/{TFE_ORG}/workspaces/{TFE_WORKSPACE}", headers = headers, verify = VERIFY)
r_ws.raise_for_status()

r_ws_data = r_ws.json()['data']
ws_id = r_ws_data['id']
ws_rc = r_ws_data['attributes']['resource-count']

print(f'Workspace name: {TFE_WORKSPACE}, id: {ws_id}, current resources: {ws_rc}')

# Find last X runs (API max page size is 100)
r_wsruns = requests.get(f"{TFE_URL}/api/v2/workspaces/{ws_id}/runs?page%5Bsize%5D={PAGESIZE}", headers = headers, verify = VERIFY)
r_wsruns.raise_for_status()
wsruns_data = r_wsruns.json()['data']

print(f'Runs retrieved: {len(wsruns_data)}')

# Extract timestamps for start and end of plan
run_ts_raw = [ (run['id'], run['attributes']['created-at'], run['attributes']['status-timestamps'].get('planning-at'), run['attributes']['status-timestamps'].get('planned-at')) for run in wsruns_data ]
# Filter out missing data
run_ts_filtered = [ x for x in run_ts_raw if (x[2] is not None) and (x[3] is not None) ]
# Parse timestamps and calculate delta
run_ts_dt = [ (x[0], x[1], datetime.datetime.strptime(x[3], TS_FORMAT) - datetime.datetime.strptime(x[2], TS_FORMAT)) for x in run_ts_filtered ]

# Print results
print()
print('run-id, created-at, duration')
for run in run_ts_dt:
    print(f'{run[0]}, {run[1]}, {run[2]}')
