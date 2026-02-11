import json
import requests

def is_work_item(item):
    return isinstance(item, dict) and 'title' in item

url = 'https://orcid.org/0000-0002-8520-7267/allWorks.json?sort=date&sortAsc=false'

response = requests.get(url)
response.raise_for_status()

data = response.json()

result = []
for group in data.get("groups", []):
    for work in group.get("works", []):
        pub_date = work.get("publicationDate") or {}
        year = pub_date.get("year")
        title_field = work.get("title") or {}
        title = title_field.get("value")
        doi = None
        eid = None
        for ext_id in work.get("workExternalIdentifiers") or []:
            id_type = (ext_id.get("externalIdentifierType") or {}).get("value", "").lower()
            id_value = (ext_id.get("externalIdentifierId") or {}).get("value")
            if id_type == "doi":
                doi = id_value
            elif id_type == "eid":
                eid = id_value
        result.append({
            "year": year,
            "title": title,
            "doi": doi,
            "eid": eid
        })

# print(json.dumps(result, ensure_ascii=False, indent=2))

with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)