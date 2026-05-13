import json
import urllib.request

url = 'https://pub.orcid.org/v3.0/0000-0002-3507-120X/works'
req = urllib.request.Request(url, headers={'Accept': 'application/json'})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

for grp in data.get('group', []):
    s = grp.get('work-summary', [{}])[0]
    title = s.get('title', {}).get('title', {}).get('value', '')
    doi = ''
    for eid in grp.get('external-ids', {}).get('external-id', []):
        if eid.get('external-id-type', '').lower() == 'doi':
            doi = eid.get('external-id-value', '')
    year = s.get('publication-date', {}).get('year', {}).get('value', '')
    type_ = s.get('type', '')
    subtype = s.get('subtype', '')
    print(year, type_, subtype, doi, title)
