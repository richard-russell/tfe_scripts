# Retrieve workspace resource counts and output sorted list (most resources first)
# NB: skeleton code ... only checks for basic errors in responses
# Reads inputs from env vars or interactively

import argparse
from getpass import getpass
import os
import requests

parser = argparse.ArgumentParser()
# parser.add_argument('-s', action='store', dest='start_time',
#                     help='Start date & time in the format: 2022-10-04T14:29:09')
# parser.add_argument('-e', action='store', dest='end_time',
#                     help='End date & time in the format: 2022-10-04T14:29:09')
parser.add_argument('start_time',
                    help='Start date & time in the format: 2022-10-04T14:29:09')
parser.add_argument('end_time',
                    help='End date & time in the format: 2022-10-04T14:29:09')
args = parser.parse_args()

PAGESIZE = 100
TS_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

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

def getallpagedata(url, headers):
    """Retrieve data from all pages of a paginated API.
       Assumes data is in 'data' and subsequent page is in next/links
    """
    # print(f'getting page: {url}')
    r = requests.get(url, headers = headers)
    r.raise_for_status()
    rj = r.json()
    data = rj.get('data')
    links = rj.get('links')
    if links is None:
        return data
    nextpage = links.get('next')
    # print(f'  nextpage -> {nextpage}')
    if nextpage is None:
        return data
    data.extend(getallpagedata(nextpage, headers))
    return data

def getrundata(url, headers, start_time):
    """Retrieve data from pages of the run API.
       If the oldest run in a page is older than the specified start time, don't request any more pages.
    """
    # print(f'getting page: {url}')
    r = requests.get(url, headers = headers)
    r.raise_for_status()
    rj = r.json()
    data = rj.get('data')
    links = rj.get('links')
    if links is None:
        return data
    if len(data) == 0:
        return data
    if data[-1]['attributes']['created-at'] < start_time:
        # print(f"Oldest run on page {data[-1]['attributes']['created-at']} is older than start time {start_time}")
        return data
    nextpage = links.get('next')
    # print(f'  nextpage -> {nextpage}')
    if nextpage is None:
        return data
    data.extend(getrundata(nextpage, headers, start_time))
    return data

# These variables are populated from environment variables if they exist, else prompt for input
TFE_URL = envorask('TFE_URL')
TFE_ORG = envorask('TFE_ORG')
TFE_TOKEN = envorask('TFE_TOKEN', sensitive=True)

headers = { "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {TFE_TOKEN}"}

# Get list of all workspaces
wslist = getallpagedata(f"{TFE_URL}/api/v2/organizations/{TFE_ORG}/workspaces?page%5Bsize%5d={PAGESIZE}", headers)
# Extract list of ws ids and names
wsids = [ (x['id'], x['attributes']['name']) for x in wslist ]

for wsid, wsname in wsids:
    wsruns = getrundata(f"{TFE_URL}/api/v2/workspaces/{wsid}/runs?page%5Bsize%5d={PAGESIZE}", headers, args.start_time)
    for run in wsruns:
        if args.start_time < run['attributes']['created-at'] < args.end_time:
            print(f"{wsname} - {run['id']} - {run['attributes']['created-at']}")



# print(f'Total workspaces: {len(wsr_sorted)}')

# print()
# print('name, resource-count')
# for ws in wsr_sorted:
#     print(f'{ws[0]}, {ws[1]}')
