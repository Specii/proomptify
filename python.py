import requests

url = "http://api.proomptify.com/generate"
headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_API_KEY"}
data = {"text": "Generate content using Proomptify."}

response = requests.post(url, headers=headers, json=data)
print(response.json())
