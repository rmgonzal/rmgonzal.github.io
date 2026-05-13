import json
import re
import urllib.parse
import urllib.request

ORCID = '0000-0002-3507-120X'
works_url = f'https://pub.orcid.org/v3.0/{ORCID}/works'
req = urllib.request.Request(works_url, headers={'Accept': 'application/json'})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

doIs = []
for grp in data.get('group', []):
    for eid in grp.get('external-ids', {}).get('external-id', []):
        if eid.get('external-id-type', '').lower() == 'doi':
            doi = eid.get('external-id-value', '').strip()
            if doi and doi not in doIs:
                doIs.append(doi)


def quote_month_fields(raw_bib):
    def repl(match):
        field, value = match.group(1), match.group(2)
        return f'{field} = {{{value}}}'

    return re.sub(r'\b(month)\s*=\s*([A-Za-z]+)\b', repl, raw_bib)

bib_entries = []
for doi in doIs:
    doi_url = 'https://doi.org/' + urllib.parse.quote(doi)
    req = urllib.request.Request(doi_url, headers={'Accept': 'application/x-bibtex; charset=utf-8'})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode('utf-8')
            raw = quote_month_fields(raw)
            if raw.strip():
                bib_entries.append(raw.strip())
                print(f'Fetched bibtex for {doi}')
            else:
                print(f'No bibtex returned for {doi}')
    except Exception as exc:
        print(f'Error fetching bibtex for {doi}: {exc}')

if bib_entries:
    with open('publications.bib', 'w', encoding='utf-8') as f:
        f.write('% Generated from ORCID 0000-0002-3507-120X\n')
        f.write('\n\n'.join(bib_entries))
    print('Wrote publications.bib with', len(bib_entries), 'entries')
else:
    print('No bibtex entries fetched')
