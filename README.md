# fhir-api-quicktools

fhir-teardown - will delete all the resources in the Azure API for FHIR instance. Warning: this should only be used for dev/learning purposes. It makes it much faster than redeployment. 

## Installation

set the following env variables:
```
FHIR_URL
FHIR_CLIENT_ID
FHIR_CLIENT_SECRET
AZ_TENANT_ID
```


```bash
pip install -r requirements.txt
cd fhir-teardown
python fhir-teardown
```

