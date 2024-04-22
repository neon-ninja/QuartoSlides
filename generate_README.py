#!/usr/bin/env python3

import os
import re
import yaml

# Define a function to extract the date and title from the YAML header of a .qmd file
def extract_info_from_yaml_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Use regular expressions to extract the date and title from YAML header
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            yaml_data = match.group(1)
            yaml_dict = yaml.load(yaml_data, Loader=yaml.FullLoader)
            date = yaml_dict.get('date', 'Invalid Date')
            title = yaml_dict.get('title', file_path[:-4])  # Use the filename as the title if not specified
            return date, title
    return 'Date not found', 'Title not found'

# Define the base URL for the links
base_url = "https://jensbri.github.io/QuartoSlides/"

# Create a list to store tuples of (date, title, markdown_link)
markdown_links = []

# Iterate through the files in the current directory
for file_name in os.listdir('.'):
    if file_name.endswith('.qmd'):
        # Extract the date and title from the YAML header
        date, title = extract_info_from_yaml_header(file_name)
        # Create a markdown link with the base URL
        markdown_link = f"[{title}]({base_url}{file_name[:-4]}#/title-slide)"
        markdown_links.append((date, title, markdown_link))

# Sort the list by date in descending order
markdown_links.sort(key=lambda x: x[0], reverse=True)


# Generate the Markdown output as a table with separate cells

markdown_output = """# QuartoSlideDecks\nRepo to host several presentations (in anti-chronological order)\n\n > [!NOTE] \n 
> These slides are created using [Quarto revealJS](https://quarto.org/docs/presentations/revealjs/) \n > [!IMPORTANT] \n 
> if you plan on reusing this template, please make sure to install relevant Quarto extensions"""
markdown_output += "| Title | Date |\n| --- | --- |\n"

for date, title, markdown_link in markdown_links:
    markdown_output += f"| {markdown_link} | {date} |\n"

# Print the Markdown output
print(markdown_output)
