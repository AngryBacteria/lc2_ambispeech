import requests

from app.data.transcripts import transcript_appendizitis

# URL for the API endpoint
url = 'http://127.0.0.1:8000/api/nlp/analyze/'

# Headers for the request
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Data to be sent in JSON format
data = {
    'text': transcript_appendizitis,
    'service': 'openai'
}

# Making the POST request
response = requests.post(url, json=data, headers=headers)

# Optional: Handling the response
print(response.status_code)
print(response.json())