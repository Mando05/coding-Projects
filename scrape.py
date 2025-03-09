import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL
base_url = 'https://drearth.com/resources/article/100-plants-you-can-grow-and-eat/'

# Send a GET request to fetch the HTML content
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(base_url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to load page {base_url}")

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store plant data
plants = []

# Find the container that holds the list of plants
plant_list_section = soup.find('div', class_='fl-col-group fl-node-boyw652r9tav fl-col-group-custom-width')
if plant_list_section:
    # Limit the number of items to process (for testing)
    max_items_to_process = 5  # Change this number as needed
    list_items = plant_list_section.find_all('li')#[:max_items_to_process]  # Limit to first 5 items
    
    for item in list_items:
        # Extract the <a> tag
        link = item.find('a')
        if not link or not link.has_attr('href'):
            print(f"Skipping item: No valid link found in {item}")
            continue
        
        # Extract plant name (text within the <a> tag)
        name = link.get_text(strip=True)
        
        # Extract the URL (href attribute of the <a> tag)
        plant_url = link['href']
        
        # Send a GET request to fetch the plant's page
        plant_response = requests.get(plant_url, headers=headers)
        if plant_response.status_code != 200:
            print(f"Failed to load plant page {plant_url}")
            continue
        
        # Parse the plant's page content
        plant_soup = BeautifulSoup(plant_response.text, 'html.parser')
        
        # Try to extract the first <p> tag from <div class="fl-rich-text">
        description_div = plant_soup.find('section', class_='entry-content article-content')
        if description_div:
            first_paragraph = description_div.find('p')  # Find the first <p> tag
            description = first_paragraph.get_text(strip=True) if first_paragraph else 'No description available'
        else:
            # If not found, try to extract the first <p> tag from <section class="entry-content article-content">
            description_section = plant_soup.find('div', class_='fl-rich-text')
            if description_section:
                first_paragraph = description_section.find('p')  # Find the first <p> tag
                description = first_paragraph.get_text(strip=True) if first_paragraph else 'No description available'
            else:
                description = 'No description available'
        
        # Extract image URL (within <img class="wpbf-post-image">)
        image_tag = plant_soup.find('img', class_='wpbf-post-image')
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'No image available'
        
        # Append the extracted data to the plants list
        plants.append({'name': name, 'description': description, 'image_url': image_url})
else:
    raise Exception("Could not find the plant list section on the page.")

# Define the CSV file name and columns
csv_file = 'plants.csv'
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