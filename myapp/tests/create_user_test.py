from cgi import test
import requests
import json
import argparse

parser = argparse.ArgumentParser(description="api testing")

parser.add_argument('--username', action='store', dest='username')
parser.add_argument('--password', action='store', dest='password')
parser.add_argument('--email', action='store', dest='email')
parser.add_argument('--firstname', action='store', dest='firstname')
parser.add_argument('--lastname', action='store', dest='lastname')

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

def test_create_user(token):

    url = "http://127.0.0.1:8000/api/users/"

    data = {"username": args.username, "password": args.password, "email": args.email, "first_name": args.firstname, "last_name": args.lastname}
    headers = {"Authorization": "Bearer " + token, "Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response)


def test_delete_user(token):

    url = "http://127.0.0.1:8000/api/users/"

    data = {"username": args.username}
    headers = {"Authorization": "Bearer " + token, "Content-type": "application/json", "Accept": "application/json"}
    response = requests.delete(url, data=json.dumps(data), headers=headers)
    print(response)


print(test_create_user(token))