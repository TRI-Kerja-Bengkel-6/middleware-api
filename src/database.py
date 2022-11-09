import mysql.connector

class MySQL(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="10.33.102.210",
            user="root",
            password="kerbengenamuser",
            port="4350",
            database="user_data"
        )
        self.mycursor = self.mydb.cursor()

    def saving(self, email, domain):
        sql = f'INSERT INTO user_domain (email, domain) VALUES (%s, %s)'
        val = (email, domain)
        try:
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except:
            pass
    
    def load(self, email):
        self.mycursor.execute(f"SELECT user_domain.domain FROM user_domain WHERE user_domain.email = '{email}';")
        res = self.mycursor.fetchall()
        result = {'domain':[]}
        for i in res:
            result['domain'].append(i[0])

        return result
