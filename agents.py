import requests, json, random
import numpy as np

# Link to localhost
url = "http://127.0.0.1:5000/orderbook"

# Get orderbook
'''
response = requests.get(url)    # To execute get request
print(response.status_code)     # To print http response code
print(response.text)
'''

# Update orderbook
'''
Send order in format:
    {"side": "B" or "A",
    "price": int} 
'''

side_choices = ["B", "A"]
price_choices = np.arange(1, 10)

# Initialize random order
side = random.choice(side_choices)
price = np.random.choice(price_choices)
data = {"side": side, "price": str(price)}
response = requests.post(url, json.dumps(data))
print(response.status_code)