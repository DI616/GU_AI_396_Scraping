import requests

user = 'guipsamora'
url = 'https://api.github.com/users/'
response = requests.get(url + user + '/repos')

response_json = response.json()
name = response_json[0]['owner']['login']
repos = []
for i in response_json:
    repos.append(i['name'])

with open('user_repos.txt', 'w') as f:
    f.write(f'User {name} has next repositories: {", ".join(repos)}.')

with open('user_repos.json', 'w') as f:
    f.write(response.text)
