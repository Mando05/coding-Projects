# send_integers.py

import requests

def send_integers_to_rpi(num1, num2):
    url = 'http://10.33.81.168:5000/send_integers'  # Replace with your Raspberry Pi IP
    data = {
        'num1': num1,
        'num2': num2
    }
    
    try:
        # Send POST request to Raspberry Pi server
        response = requests.post(url, json=data)
        
        # Handle the response from the server
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.json())

    except requests.exceptions.RequestException as e:
        print("Failed to send data:", str(e))

# Example call to send integer
