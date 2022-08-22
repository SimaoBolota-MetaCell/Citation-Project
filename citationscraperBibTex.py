
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
import yaml
from pycff import pycff


# takes url input and stores HTML of page
html = requests.get( 'https://github.com/juglab/PlatyMatch/blob/master/README.md').text
# html = requests.get( 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README.md').text
# html = requests.get(
#     'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README2.md').text
soup = BeautifulSoup(html, 'html5lib')
# print(soup)  # check if page HTML is correct

paragraphs = soup.find_all("p", {'dir': 'auto'})
paragraphs = str(paragraphs)
# print(paragraphs) # check if right elements

snippets = soup.find_all("div", {
                         'class': 'highlight highlight-text-bibtex notranslate position-relative overflow-auto'})
snippets = str(snippets)
# print(snippets)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



# BIBTEX CITATIONS
BibTex_text = strip_tags(snippets)
BibTex_text = BibTex_text.replace("\xa0", " ")
BibTex_text = BibTex_text.replace("=", " = ")
BibTex_text = BibTex_text.replace("]", " }")
BibTex_text = BibTex_text.replace("{\\~a}", "ã")
BibTex_text = BibTex_text.replace("{\\'a}", "á")
BibTex_text = re.sub(' +', ' ', BibTex_text)
# print(BibTex_text)

bibtex_pattern = '(?<=@)(.*?)(?=\}\s*\})'

all_bibtex_citations = re.findall(bibtex_pattern, BibTex_text, flags=re.DOTALL)


if all_bibtex_citations:
    for citation in all_bibtex_citations:
        citation = re.sub('"', '}', citation)
        citation = re.sub('= }', '= {', citation)
        print('FULL CITATION :')
        print(citation)
        print('\n')


        author = re.findall(
            '(?<=author\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if author:
           author_string = ' '.join(map(str, author))
           individual_author = re.findall("(?:[A-Z][A-Za-z'`-]+,)" + "\\s[A-Z][A-Za-z'`-]+" , author_string, flags=re.DOTALL)
           individual_author_string = ' '.join(map(str, individual_author))

           family_names = re.findall("(?:[A-Z][A-Za-z'`-]+,)" , individual_author_string, flags=re.DOTALL)
           family_names = ' '.join(map(str, family_names))
           family_names = family_names.replace(",", "")

           given_names =re.findall("(,\\s[A-Z][A-Za-z'`-]+)" , individual_author_string, flags=re.DOTALL)
           given_names = ' '.join(map(str, given_names))
           given_names = given_names.replace(", ", "")

           print('AUTHORS GIVEN NAMES')
           print(given_names ) 
           print('\n')
           print('AUTHORS FAMILY NAMES')
           print(family_names)
           print('\n')


        year = re.findall(
            '(?<=year\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if year:
            print('YEAR')
            print(year)
            print('\n')

        title = re.findall(
            '(?<=title\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if title:
            print('TITLE ')
            print(title)
            print('\n')

        publisher = re.findall(
            '(?<=publisher\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if publisher:
            print('PUBLISHER found')
            print(publisher)
            print('\n')

        doi = re.findall(
            '(?<=doi\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if doi:
            print('DOI found')
            print(doi)
            print('\n')

        url = re.findall(
            '(?<=URL\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if url:
            print('URL found')
            print(url)
            print('\n')

        journal = re.findall(
            '(?<=journal\\s=\\s\{)(.*?)(?=\},)', citation, flags=re.DOTALL)
        if journal:
            print('JOURNAL found')
            print(journal)
            print('\n')


# USING PYYAML

        title_string = ''.join(map(str, title))
        publisher_string = ''.join(map(str, publisher))
        year_string = ''.join(map(str, year))
        doi_string = ''.join(map(str, doi))


        dict_file = {'cff-version': '1.2.0',
                     'message': 'If you use this plugin, please cite it using these metadata',
                     'authors': [{'family-names': family_names}, {'given_names': given_names}],
                     'title': title_string,
                     'doi': doi_string,
                     'date-released': year_string}

        with open(r'./Citation-Project/CITATION.cff', 'w') as file:
            documents = yaml.dump(dict_file, file, sort_keys = False)


# USING PYCFF - not working
# text = (
#             '# YAML 1.2\n'
#             '---\n'
#             'cff-version: "1.1.0"\n'
#             'message: Do cite this\n'
#             'title: Testing CFF!\n'
#             'version: 0.0.1\n'
#             'authors: []\n'
#             'date-released: 2020-11-15 00:00:00\n')

# cff = pycff.load(text)




# NOTES and QUESTIONS
# - BIBTEX can start with another thing other than @article
# - APA Citations formatting, change the way the pattern is being recognized
# - multiple citations, in what key to put the information and how
# - re-check the order for family names and given names