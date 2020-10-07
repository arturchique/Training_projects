import requests

a = requests.get('http://157.245.77.126/s2b/api/v1/hello/').json()

print(a)