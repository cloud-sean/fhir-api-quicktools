import requests
import json
import config


def _get_auth_token() -> str:
    url = f"https://login.microsoftonline.com/{config.AZ_TENANT_ID}/oauth2/token"
    payload = f'grant_type=client_credentials&client_Id={config.FHIR_CLIENT_ID}&client_secret={config.FHIR_CLIENT_SECRET}&resource={config.FHIR_URL}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    return res['access_token']
