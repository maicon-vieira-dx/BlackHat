import requests

url = "https://akipromotora.com.br"
response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print("Erro ao acessar a URL:", response.status_code)