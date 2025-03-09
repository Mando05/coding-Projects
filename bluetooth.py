import requests

# Replace with the Raspberry Pi's IP address
raspberry_pi_ip = 'http://10.33.81.168:5000'

def turn_led_on():
    response = requests.get(f"{raspberry_pi_ip}/motor/on")
    print(response.text)

def turn_led_off():
    response = requests.get(f"{raspberry_pi_ip}/motor/off")
    print(response.text)

# Example usage:
turn_led_off()  # Turn LED on
