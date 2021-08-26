import os
import requests
import json
from tqdm import tqdm
import config
from util import _get_auth_token

access_token = _get_auth_token()

headers = {
    'Content-Type': 'application/fhir+json; charset=utf-8',
    'Authorization': f'Bearer {access_token}'
}


def execute_delete(resource_pack, recall=False):
    payload = json.dumps({
        "resourceType": "Bundle",
        "type": "batch",
        "entry": resource_pack
    })
    response = requests.request(
        "POST", url=config.FHIR_URL, data=payload, headers=headers)

    if recall:
        print('Batch Complete, starting next...')
        return get_resource_bundles()
    else:
        print('Completed')


def get_total_records():
    total = requests.request(
        "GET", url=f"{config.FHIR_URL}?_summary=count", headers=headers)

    return (total.json()['total'])


def get_resource_bundles():
    resources_bundle = []
    recall = False
    total = get_total_records()

    # FHIR API limit for Batch instruction size
    if total > 499:
        total = 499
        # flag to run the method again
        recall = True
    elif total < 1:
        print('No remaining records. Done!')
        quit()

    all_resources = requests.request(
        "GET", url=f"{config.FHIR_URL}?_elements=fullUrl&_count=1000", headers=headers).json()['entry']

    for res in tqdm(range(total), desc="Loading..."):
        relative_location = all_resources[res]['fullUrl'].replace(
            f'{config.FHIR_URL}/', '')
        resources_bundle.append({
            "request": {
                "method": "DELETE",
                "url": relative_location
            }
        })
        # if we have more than 500 resources we run this function again from execute_delete()
    execute_delete(resources_bundle, recall=recall)


if __name__ == "__main__":
    get_resource_bundles()
