import requests
from bs4 import BeautifulSoup
import csv

# Define the URL
url = 'https://www.gardencentermarketing.com/Top-100-Plant-Downloads'

# Send a GET request to fetch the HTML content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store plant data
plants = []

# Find the container that holds the plant information
plant_list_section = soup.find('div', class_='plant-list')
if plant_list_section:
    # Iterate over each plant item
    plant_items = plant_list_section.find_all('div', class_='plant-item')
    for plant in plant_items:
        # Extract plant name
        name_tag = plant.find('h2')
        name = name_tag.text.strip() if name_tag else 'No name available'
        
        # Extract plant description
        description_tag = plant.find('p', class_='description')
        description = description_tag.text.strip() if description_tag else 'No description available'
        
        # Extract image URL
        image_tag = plant.find('img')
        image_url = image_tag['src'].strip() if image_tag and 'src' in image_tag.attrs else 'No image available'
        
        # Append the extracted data to the plants list
        plants.append({'name': name, 'description': description, 'image_url': image_url})
else:
    raise Exception("Could not find the plant list section on the page.")

# Define the CSV file name and columns
csv_file = 'top_100_plants.csv'
csv_columns = ['name', 'description', 'image_url']

# Write the data to the CSV file
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for plant in plants:
            writer.writerow(plant)
    print(f"Data successfully written to {csv_file}")
except IOError as e:
    print(f"I/O error occurred: {e}")
