import requests

key = 'aIPWtG7eKnqSpE83d24JvDOHLihQAgN6'
params = {'page': 1, 'pageSize': 10, 'apiKey': key}
url = 'https://core.ac.uk:443/api-v2/search/astronomy'

response = requests.get(url, params=params)

with open('core_response.json', 'w') as f:
    f.write(response.text)
