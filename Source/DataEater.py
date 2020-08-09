import psycopg2
import json
import os

files = [json.load(open('./Models/' + f))['ObjectStates'] for f in os.listdir('./Models/')]
connection = psycopg2.connect(user=os.environ.get('SQL_USER'),
                              password=os.environ.get('SQL_PASSWORD'),
                              host=os.environ.get('SQL_HOST'),
                              port=os.environ.get('SQL_PORT'),
                              database=os.environ.get('SQL_NAME'))
cursor = connection.cursor()
models = []
for file in files:
    for model in file:
        if model['Name'] == 'Custom_Model':
            model['Transform']['posX'] = 0.0
            model['Transform']['posY'] = 0.0
            model['Transform']['posZ'] = 0.0
            model['Transform']['rotX'] = 0.0
            model['Transform']['rotY'] = 0.0
            model['Transform']['rotZ'] = 0.0
            for i, c in enumerate(model['Nickname']):
                if c.isdigit():
                    model['Nickname'] = model['Nickname'][:i]
                    break
                elif c == '-':
                    index = i
                    for k in range(i, 0, -1):
                        if model['Nickname'][k] == ' ':
                            index = k
                            break
                    model['Nickname'] = model['Nickname'][:index]
                    break
                elif c == '/':
                    index = i
                    for k in range(i, 0, -1):
                        if model['Nickname'][k] == ' ':
                            index = k
                            break
                    model['Nickname'] = model['Nickname'][:index]
                    break
                elif c == '(':
                    index = i
                    for k in range(i, 0, -1):
                        if model['Nickname'][k] == ' ':
                            index = k
                            break
                    model['Nickname'] = model['Nickname'][:index]
                    break
            cursor.execute("SELECT nickname FROM models WHERE nickname = %s;", (model['Nickname'].lower().replace('-', '').replace(' ', '').replace('/', ''),))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO models (nickname, skeleton) VALUES (%s,%s)",
                               (model['Nickname'].lower().replace('-', '').replace(' ', '').replace('/', ''), json.dumps(model)))
            connection.commit()



