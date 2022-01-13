import requests
import json
import argparse

parser = argparse.ArgumentParser(description="api testing")

parser.add_argument('--username', action='store', dest='username')
parser.add_argument('--password', action='store', dest='password')
parser.add_argument('--severity', action='store', dest='severity')
parser.add_argument('--timestamp', action='store', dest='time')
parser.add_argument('--projectname', action='store', dest='projname')
parser.add_argument('--content', action='store', dest='logcont')

args = parser.parse_args()


#authenticate and obtain jwt for further requests authentication
#returns 2 tokens, access and refresh
def get_token(username, password):
    url = "http://127.0.0.1:8000/api/token/"
    data = {"username": username, "password": password}
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(response.content)


def refresh_token(token):
    url = "http://127.0.0.1:8000/api/token/refresh/"
    data = {"refresh": token}
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(response.content)

token = (get_token(args.username, args.password)['access'])
#populate database with valid entries
def populate_database(token):
    url = "http://127.0.0.1:8000/api/addlogs/"

    data = [{"user": args.username,
            "sevlevel": args.severity,
            "time": args.time,
            "projname": args.projname,
            "logcont": args.logcont}]

    responses = []
    print('Populating database...')
    for post in data:
        headers = {'Authorization': 'Bearer ' + token, "Content-type": "application/json", "Accept": "application/json"}
        response = requests.post(url, data=json.dumps(post), headers=headers)
        responses.append(response)

    return responses


print(populate_database(token))
