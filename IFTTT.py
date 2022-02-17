import requests

API_KEY = 'c959eBOk46PWwCEsO3jCyP'

def trigger_event(evName, evCode, text):
    url = f'https://maker.ifttt.com/trigger/{evName}/with/key/{API_KEY}'
    report = {}
    report['value1'] = evCode
    report['value2'] = text
    requests.post(url, data=report)