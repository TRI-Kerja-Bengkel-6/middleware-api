import requests
import json

def login():
    url = "https://admin.kerbengenam.my.id/api/auth"

    payload = json.dumps({
    "password": "kerjabengkel6",
    "username": "admin"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    res = response.json()

    return res

def createStack():
    url = "https://admin.kerbengenam.my.id/api/stacks"

    payload={'type': '1',
            'method': 'file',
            'endpointId': '3',
            'Name': 'wordpress-client1',
            'SwarmID': '29o5t7fpff07hwj7s4g65ruvr'}
    files=[('file',('docker-compose.yml',open('/C:/Users/komjar2/Desktop/docker-compose.yml','rb'),'application/octet-stream'))]
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsInNjb3BlIjoiZGVmYXVsdCIsImZvcmNlQ2hhbmdlUGFzc3dvcmQiOmZhbHNlLCJleHAiOjE2NjczODMwMTcsImlhdCI6MTY2NzM1NDIxN30.oceqflmJw7pK9qM_F_m5ONq2pFHU18fsyZneQP4-QT4'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


if __name__ == '__main__':
    print(login()['jwt'])
