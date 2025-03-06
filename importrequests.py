import requests

def submitform(data):
    url = r'https://prod-253.westeurope.logic.azure.com:443/workflows/53ca985c34f849cb8630367a69cb4b9b/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=roxQ3UPK9qlfMsnrTcgCO_knugF7yyytG1qpjzSazp8'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    requests.post(url, json=data, headers=headers)

