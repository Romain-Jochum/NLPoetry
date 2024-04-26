"""
We used web scraping to collect your data to finetune Mistral 7B LLM, here is the code used
The data is scraped from poesie-francaise.fr on the 21 of April 2024
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

"""
author_links_scraper() has no argument and return a list containing the links its from the source code of the following
web page https://www.poesie-francaise.fr/poemes-themes/ of the poems authors web page. We could have done it such that 
it directly scrape from the web page it-self but less work, same result make dum monkey happy 🐒.
exemple of output: ["https://my-super-link/apollinaire.com", "https://my-super-link/baudelaire.com", ...]
"""


def author_links_scraper():
    try:
        # Read the HTML code from the text file
        with open(source_code_txt_path, "r") as file:
            html_code = file.read()

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find all 'ul' elements with class 'reglage-menu'
        ul_elements = soup.find_all('ul', class_='reglage-menu')

        # Initialize an empty list to store author links
        author_list = []

        # Loop through each 'ul' element to extract author links
        for ul in ul_elements:
            # Find all 'a' tags within the 'ul' element
            author_tags = ul.find_all('a')
            # Extract the href attribute from each 'a' tag and append to author_links list
            for author_tag in author_tags:
                author_list.append(author_tag['href'])

        # Print the list of author links
        return author_list

    except FileNotFoundError:
        print(f"Error: File '{source_code_txt_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


"""
scrape_poem_links() take a list containing strings (the links of the webpage with all the poems of the same theme).
exemple of input: ["https://my-super-link/apollinaire.com", "https://my-super-link/baudelaire.com", ...]

It will go through each of the links, scrape the poems links from each author and return a list of tuples containing the 
links to the poems webpages and its theme.
exemple of output: ["https://my-super-link/apollinaire/poem1.com", "https://my-super-link/apollinaire/poem2.com", ...]
"""


def scrape_poem_links(author_list):
    poem_list = []
    # Loop through each author link
    for author_link in author_list:
        response = requests.get(author_link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all elements with class "w3-panel"
        poem_elements = soup.find_all('div', class_='w3-panel')

        # Extract poem links
        for poem_element in poem_elements:
            poem_link = poem_element.find('a')['href']
            poem_list.append(poem_link)
    return poem_list


"""
check_and_scrape_poem() take a strings (link) as input.
exemple of input: "https://my-super-link/apollinaire/poem1.com"

It will return nothing but during the execution it will add to the global variables authors, titles, books, years and 
poems the corresponding information relative to the given poem linked, if one of the information isn't available it will
just print the corresponding error in the terminal
"""


def check_and_scrape_poem(poem_link):
    try:
        response = requests.get(poem_link)
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
            authors.append(author)
            titles.append(title)
            books.append(book)
            years.append(year)
            poems.append(poem_text)
        else:
            print(f"Skipping link: {poem_link}")
    except Exception as e:
        print(f"Error: {e}")


"""
df_builder() take as argument a list of strings (links) like such:
exemple of input: ["https://my-super-link/apollinaire/poem1.com", "https://my-super-link/apollinaire/poem2.com", ...]

This function will build and return a pandas dataframe containing the information of all the poems (authors, titles,
books, years and poems it-self)
"""


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
        'Title': titles,
        'Year': years,
        'Poem': poems
    })
    return dataframe


""" 
Time for fun, here we instantiate the global variables required to run our custom functions and than after we use the 
functions to build a csv file containing the data we are interested in, they are not yet cleaned at this point
"""


theme_list = []
authors = []
books = []
years = []
poems = []
titles = []
source_code_txt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_code.txt")

# the activation line
df_builder(scrape_poem_links(author_links_scraper())).to_csv('poem_data.csv', index=False)

print("DataFrame saved to CSV file.")
