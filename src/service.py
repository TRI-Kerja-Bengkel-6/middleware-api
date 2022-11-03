from src.portainer import login, createStack

def service(username, password, app, subdomain):
    if app.lower() == 'wordpress':
        template = './templates/wordpress.yml'
    else:
        return {'err': 'Template tidak ditemukan'}

    token = login('admin','kerjabengkel6')['jwt']
    
    res = createStack(username, app, template, token, subdomain=subdomain, db_password=password or '')

    return res

# if __name__ == '__main__':
#     res = service('hanung', 'hanung2501', 'wordpress', 'hanung')