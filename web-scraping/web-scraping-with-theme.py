"""
We used web scraping to collect your data to finetune Mistral 7B LLM, here is the code used
The data is scraped from poesie-francaise.fr on the 21 of April 2024
"""
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the file path relative to the script's directory
source_code_txt_path = os.path.join(script_dir, "source_code_for_theme.txt")


def author_links_scraper():
    try:
        # Read the HTML code from the text file
        with open(source_code_txt_path, "r") as file:
            html_code = file.read()

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find all 'ul' elements with class 'reglage-menu'
        ul_elements = soup.find_all('ul', class_='reglage-menu')

        # Initialize an empty list to store theme links

        # Loop through each 'ul' element to extract author links
        for ul in ul_elements:
            # Find all 'a' tags within the 'ul' element
            theme_tags = ul.find_all('a')
            # Extract the href attribute from each 'a' tag and append to author_links list
            for theme_tag in theme_tags:
                theme_list.append((theme_tag['href'], theme_tag.text))

        # Print the list of author links
        return theme_list

    except FileNotFoundError:
        print(f"Error: File '{source_code_txt_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def scrape_poem_links(themes_list):
    poem_list = []
    # Loop through each author link
    for theme_link in themes_list:
        response = requests.get(theme_link[0])
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all elements with class "w3-panel"
        poem_elements = soup.find_all('div', class_='w3-panel')
        theme = soup.find('x')

        # Extract poem links
        for poem_element in poem_elements:
            poem_link = poem_element.find('a')['href']
            poem_list.append((poem_link, theme_link[1]))
    return poem_list


# Function to check link status and scrape poem content
def check_and_scrape_poem(poem_link):
    try:
        response = requests.get(poem_link[0])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find element with class "w3-content" which contains poem information
            poem_content = soup.find('div', class_='w3-content')

            # Extract poem title, author, book, year, and content
            title = poem_content.find('h2').text.strip()
            title = title.replace('Titre : ', '')
            author = poem_content.find('h3').text.split('Poète : ')[1].split(' (')[0].strip()
            book_info = poem_content.find('div', class_='w3-margin-bottom').text.strip()
            book = book_info.split('Recueil : ')[1].split(' (')[0].strip()
            year = book_info.split(' (')[1].split(').')[0].strip()
            poem_text_elements = poem_content.find_all('p')
            pattern = r'<br\s*/*>|\n'
            poem_text = '\n'.join(
                [re.sub(pattern, lambda m: '\n' if m.group().startswith('<br') else '', str(elem)) for elem in
                 poem_text_elements])
            poem_text = BeautifulSoup(poem_text, 'html.parser').text

            # Append data to respective lists
            themes.append(poem_link[1])
            authors.append(author)
            titles.append(title)
            books.append(book)
            years.append(year)
            poems.append(poem_text)
        else:
            print(f"Skipping link: {poem_link[0]}")
    except Exception as e:
        print(f"Error: {e}")


# Loop through each poem link and check/scrape content
def df_builder(poem_list):
    i = 0
    for poem_link in poem_list:
        i += 1
        print(f"Try poem n°{i}")
        check_and_scrape_poem(poem_link)

    # Create a dataframe with the scraped data
    dataframe = pd.DataFrame({
        'Author': authors,
        'Book': books,
        'Year': years,
        'Title': titles,
        'Theme': themes,
        'Poem': poems
    })
    return dataframe


""" Time for fun"""
theme_list = []
authors = []
books = []
years = []
poems = []
titles = []
themes = []

author_links = author_links_scraper()
poem_links = scrape_poem_links(author_links)
df = df_builder(poem_links)
df.to_csv('poem_data.csv', index=False)

print("DataFrame saved to CSV file.")
