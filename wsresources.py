# Retrieve workspace resource counts and output sorted list (most resources first)
# NB: skeleton code ... only checks for basic errors in responses
# Reads inputs from env vars or interactively

from getpass import getpass
import os
import requests

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
    """Retrieve data from all pages of a paginated URL.
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

# These variables are populated from environment variables if they exist, else prompt for input
TFE_URL = envorask('TFE_URL')
TFE_ORG = envorask('TFE_ORG')
TFE_TOKEN = envorask('TFE_TOKEN', sensitive=True)

headers = { "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {TFE_TOKEN}"}

# Get list of all workspaces
wslist = getallpagedata(f"{TFE_URL}/api/v2/organizations/{TFE_ORG}/workspaces?page%5Bsize%5d={PAGESIZE}", headers = headers)
# Extract resource count
wsresources = [ (ws['attributes']['name'], ws['attributes']['resource-count']) for ws in wslist ]
wsr_sorted = sorted(wsresources, key=lambda x:x[1], reverse=True)

print(f'Total workspaces: {len(wsr_sorted)}')

print()
print('name, resource-count')
for ws in wsr_sorted:
    print(f'{ws[0]}, {ws[1]}')
