import requests
import json
import argparse

parser = argparse.ArgumentParser(description="api testing")

parser.add_argument('--adminuser', action='store', dest='adminuser')
parser.add_argument('--adminpass', action='store', dest='adminpass')
parser.add_argument('--username', action='store', dest='username')

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


token = (get_token(args.adminuser, args.adminpass)['access'])

def test_delete_user(token):

    url = "http://127.0.0.1:8000/api/users/"

    data = {"username": args.username}
    headers = {"Authorization": "Bearer " + token, "Content-type": "application/json", "Accept": "application/json"}
    response = requests.delete(url, data=json.dumps(data), headers=headers)
    print(response)


print(test_delete_user(token))