"""
We used web scraping to collect your data to finetune Mistral 7B LLM, here is the code used
The data is scraped from poesie-francaise.fr on the 23 of April 2024
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

"""
author_links_scraper() has no argument and return a list of tuples containing the theme and its href links from the
source code of the following web page https://www.poesie-francaise.fr/poemes-themes/ . We could have done it such that 
it directly scrape from the web page it-self but less work, same result make dum monkey happy 🐒.
exemple of output: [("love","https://my-super-link/love.com"),("hate","https://my-super-link/hate.com"),...]
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


"""
scrape_poem_links() take a list of tuples (or list since it also works with list) containing two strings (theme of the 
poems and the links of the webpage with all the poems of the same theme).
exemple of input: [("love","https://my-super-link/love.com"),("hate","https://my-super-link/hate.com"),...]

It will go through each of the links, scrape the poems links in each theme and return a list of tuples containing the 
links to the poems webpages and its theme.
exemple of output: [("love","https://my-super-link/love/poem1.com"),("hate","https://my-super-link/hate/poem1.com"),...]
"""


def scrape_poem_links(themes_list):
    poem_list = []
    # Loop through each author link
    for theme_link in themes_list:
        response = requests.get(theme_link[0])
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all elements with class "w3-panel"
        poem_elements = soup.find_all('div', class_='w3-panel')

        # Extract poem links
        for poem_element in poem_elements:
            poem_link = poem_element.find('a')['href']
            poem_list.append((poem_link, theme_link[1]))
    return poem_list


"""
check_and_scrape_poem() take a tuples of two strings.
exemple of input: ("love","https://my-super-link/love.com")

It will return nothing but will add to the global variables themes, authors, titles, books, years and poems the 
corresponding information relative to the given poem linked, if one of the information isn't available it will just 
print the corresponding error in the terminal
"""


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


"""
df_builder() take as argument a list of tuples like such:
exemple of input: [("love","https://my-super-link/love/poem1.com"),("hate","https://my-super-link/hate/poem1.com"),...]

This function will build and return a pandas dataframe containing the information of all the poems (themes, authors, 
titles, books, years and poems it-self)
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
        'Year': years,
        'Title': titles,
        'Theme': themes,
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
themes = []
source_code_txt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_code_for_theme.txt")

# the activation line
df_builder(scrape_poem_links(author_links_scraper())).to_csv('poem_data_with_theme.csv', index=False)

print("DataFrame saved to CSV file.")
