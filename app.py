import requests, json
import IFTTT
from datetime import datetime, timedelta
import collections
# Constants
IFTTT_EVNAME = 'ReuniwattSrv'
ANTARES_API_KEY = '1353a13e-cdc4-4f03-93de-3fb1f04fe4c3'
ANTARES_API_SECRET = 'd26753d9-42d4-4098-9f1a-4f40046ac5ef'

# Globals
properties_dict = {
        'dni':'40666aca-81ff-407e-b44e-9a06c185af62',
        'ghi':' b3f78769-74ff-45b4-8247-44ff52695e76',
        'wind_speed_10m':'5f0b26c4-03b3-40d2-8a98-2790cdda6345',
        'dhi':'43b3af32-59ca-4ee7-9f1f-62fd69b10ef6',
        'gti_trk':'6ff34c5d-68d3-4a0f-b825-1eda5db8bcec',
        'temperature_2m':'888da8ee-df2b-4283-babe-272b6e7aeef9',
        'relative_humidity_2m':'2d9d5466-f6e6-4cd3-809f-378d256a42b2'	
    }


# from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
# to_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

api_url = f'https://api.reuniwatt.com/v1/baywa-donrodrigo2-daycast-saidea'
antares_url = 'https://trustpv.goantares.uno/public/api/v3/ServicePortfolios/fd75561b-9821-47e0-974d-c55cdb1ff4b8/Properties'

def main():
    # Request data
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJpc3MiOiJodHRwczovL2F1dGhhcGkwMS5zb2xla2Eub3JnIiwiaWF0IjoxNjQ0NTc2NTk4LCJleHAiOjE3MjUyMzUyMDAsInN1YiI6ImJiYXNzb252aWxsZSIsImp0aSI6IjEyZDY3NGU1LTk4NjctNDRhMS1iMDIzLTAzYWI1MjA4MTA3YiIsImxvY2F0aW9uX2Nvb3JkaW5hdGVzIjpudWxsLCJsb2NhdGlvbl9jb3VudHJpZXMiOm51bGwsInBlcmlvZCI6bnVsbCwic2NvcGUiOlsiUkVBRF9QUk9EVUNUX0JBWVdBLURPTlJPRFJJR08yLURBWUNBU1QiXSwidXNhZ2UiOiJiYXl3YS1kb25yb2RyaWdvMi1kYXljYXN0In0.AF13wFOiPUJDyUp00iBumTxP1o_n6NdrwbQoNyUiEIPfVdKIajselJ9uYJ-0QjvkkM6-0GzOdq4pooVOG39v_9PdATYoqGtXJ7WUCeunfi27otPdJNbukZosclhkIxm6frIMjLHPw1VnqTWVBp_E53ygv96j7ljtJBnDu2XD4u-fyRm9"}
    res = requests.get(api_url, headers=headers)
    if res.status_code != 200:
        text = f'''<br>
                        Message: Error {res.status_code} getting data from API.<br>
                    '''
        IFTTT.trigger_event(IFTTT_EVNAME, 'GetDataError', text)
    data = res.json()
    # Get last record
    indicators = data['DonRodrigo2']

    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    for property_name, property_id in properties_dict.items():
        values = indicators[property_name]
        for key, value in values.items():
            body_request = {
                "Value": str(value),
                "TypeId": property_id,
                "RelatedEntityId": property_id,
                "RelatedEntityType": 1,
            }
            body_request = json.dumps(body_request)
            res = requests.post(url=antares_url, headers=headers, data=body_request, auth=(ANTARES_API_KEY, ANTARES_API_SECRET))

            #IFTT
            if res.status_code != 200:
                text = f'''<br>
                            Message: Error {res.status_code} sending POST request to Antares.<br>
                            Property: {property_name}<br>
                            Value: {value}
                        '''
                IFTTT.trigger_event(IFTTT_EVNAME, 'AntaresInsertError', text)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        IFTTT.trigger_event(IFTTT_EVNAME,'Exception', e)