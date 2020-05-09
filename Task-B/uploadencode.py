import requests

username = input('Enter username: ')
files = {'encoding':open('encodings.pickle', 'rb')}
data = {'username': username}
request = requests.post('http://192.168.1.225:5000/addfrencoding',files=files, data=data)
print(request.text)