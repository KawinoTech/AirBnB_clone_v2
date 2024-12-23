import requests

url = 'https://validator.w3.org/nu/'
headers = {'Content-Type': 'text/html; charset=utf-8'}
file_path = 'path/to/file.html'

with open(file_path, 'r') as file:
    response = requests.post(url, headers=headers, data=file)
    print(response.text)
