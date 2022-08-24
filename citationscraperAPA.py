from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
import yaml
from pycff import pycff


# takes url input and stores HTML of page
# html = requests.get( 'https://github.com/SanderSMFISH/napari-buds/blob/main/README.md').text
html = requests.get(
    'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README.md').text
# html = requests.get(
#     'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README2.md').text
soup = BeautifulSoup(html, 'html5lib')
# print(soup)


# APA citations are either created as normal text or listed items
paragraphs = soup.find_all("p", {'dir': 'auto'})
paragraphs = str(paragraphs)

lists = soup.find_all("li")
lists = str(lists)


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


# # APA CITATIONS

APA_text = strip_tags(paragraphs)  # strip HTML
APA_text = APA_text.replace("\xa0", " ")  # for stray strings
APA_text = re.sub('\.\\s\w\.', '.', APA_text)
print('APATEXT:' + APA_text)

# REGEX PATTERNS

authors = "(?:[A-Z][A-Za-z'`-]+)" + ", " + "(?:\w\.)"
year_num = '\(([0-9]{4})\)'

title = '(?:\.)(.*?)(?=\.)'
doi = '(?:doi.org/)(.*?)(?=,)'

all_apa_authors = re.findall(authors, APA_text, flags=re.DOTALL)
all_apa_authors = ', '.join(all_apa_authors)
print('ALL AUTHORS:' + all_apa_authors)


apa_pattern_wo_authors = year_num + "(.*?)" + doi

all_apa_citations = re.findall(
    apa_pattern_wo_authors, APA_text, flags=re.DOTALL)
for citation in all_apa_citations:
    citation = ''.join(map(str, citation))
    citation = re.sub('\(', '', citation)
    citation = all_apa_authors + ' ' + citation
    print('CITATION:')
    print(citation)
    print('\n')
    print('AUTHORS:')
    print(all_apa_authors)
    print('\n')

    family_names = re.findall(
        "(?:[A-Z][A-Za-z'`-]+,)", all_apa_authors, flags=re.DOTALL)
    family_names = [w.replace(',', '') for w in family_names]

    given_names = re.findall(
        "(\,\\s[A-Z]\.)", all_apa_authors, flags=re.DOTALL)
    given_names = [w.replace(', ', '') for w in given_names]

    print('AUTHORS GIVEN NAMES')
    print(given_names)
    print('\n')
    print('AUTHORS FAMILY NAMES')
    print(family_names)
    print('\n')

    citation_year = re.findall('(\\s[0-9]{4}\.)', citation, flags=re.DOTALL)
    citation_year = [w.replace('.', '') for w in citation_year]
    citation_year = [w.replace(' ', '') for w in citation_year]
    citation_year = ''.join(map(str, citation_year))


    print('YEAR')
    print(citation_year)
    print('\n')

    citation_title = re.findall(
        '(?:[0-9]{4}\.\\s)([A-Z].*?)(?=\.)', citation, flags=re.DOTALL)
    print('TITLE')
    print(citation_title)
    print('\n')

    citation_title = ' '.join(map(str, citation_title))
    citation_journal = re.findall(citation_title +'.'+ '(.*?)(?:doi)', APA_text, flags=re.DOTALL)
    print('JOURNAL')
    print(citation_journal)
    print('\n')

    citation_doi = re.findall(doi, APA_text, flags=re.DOTALL)
    print('DOI')
    print(citation_doi)
    print('\n')


# USING PYYAML

    dict_file = {'cff-version': '1.2.0',
                     'message': 'If you use this plugin, please cite it using these metadata',
                     'authors': [{'family-names': family_names, 'given-names': given_names}],
                     'title': citation_title,
                     'references' : [{'year':citation_year, 'journal': citation_journal}],
                     'doi': citation_doi,
                     'date-released': citation_year + '-01-01',
                     'references' : [{'type':'book', 'publisher':[{'name':'publisher'}]}]
}

    with open(r'./Citation-Project/aCITATION.cff', 'w') as file:
            documents = yaml.dump(dict_file, file, sort_keys = False)
