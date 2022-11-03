import requests
import json

def login(username,password):
    url = "https://admin.kerbengenam.my.id/api/auth"

    payload = json.dumps({
    "password": password,
    "username": username
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    res = response.json()

    return res

def createStack(name, app, template, token, subdomain, db_password):
    url = "https://admin.kerbengenam.my.id/api/stacks"

    payload={
        'type': '1',
        'method': 'file',
        'endpointId': '3',
        'Name': name,
        'SwarmID': '29o5t7fpff07hwj7s4g65ruvr',
        'Env': json.dumps([
            {'name': 'SUBDOMAIN', 'value': f'{subdomain}'},
            {'name': 'WORDPRESS_DB_PASSWORD', 'value': f'{db_password}'}
        ])
    }
    files=[('file',(f'{app}.yml',open(template,'rb'),'application/octet-stream'))]
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    result = response.json()

    if response.status_code == 200:
        output = {'status': 'successful',
                  'app_domain': f'{subdomain}.kerbengenam.my.id',
                  'phpmyadmin (if any)': f'{subdomain}.phpmyadmin.kerbengenam.my.id',
                  'info': "if the webservice can't be accessed, pls wait atleast 1 minute. please contact admin@kerbengenam.my.id if there's still a problem",
                  'response': result}
    else:
        output = {'status': 'unsuccessfull',
                  'response': result}

    return output


# if __name__ == '__main__':
#     print(login('admin','kerjabengkel6')['jwt'])
