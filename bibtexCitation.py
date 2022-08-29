
import re
from htmlScraper import *




def get_bibtex_citations(link):

    soup = get_html(link )
    snippets = soup.find_all("div", {
                         'class': 'highlight highlight-text-bibtex notranslate position-relative overflow-auto'})
    snippets = str(snippets)

    BibTex_text = strip_tags(snippets)
    BibTex_text = BibTex_text.replace("\xa0", " ")
    BibTex_text = BibTex_text.replace("=", " = ")
    BibTex_text = BibTex_text.replace("]", " }")
    BibTex_text = BibTex_text.replace("{\\~a}", "ã")
    BibTex_text = BibTex_text.replace("{\\'a}", "á")
    BibTex_text = re.sub(' +', ' ', BibTex_text)

   
    bibtex_pattern = '(?<=@)(.*?)(?=\}\s*\})'

    all_bibtex_citations = re.findall(bibtex_pattern, BibTex_text, flags=re.DOTALL)

    return all_bibtex_citations



def get_bibtex_family_names(individual_citation):
    
    author = re.findall(
            '(?<=author\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    if author:
           author_string = ' '.join(map(str, author))
           individual_author = re.findall("(?:[A-Z][A-Za-z'`-]+,)" + "\\s[A-Z][A-Za-z'`-]+" , author_string, flags=re.DOTALL)
           individual_author_string = ' '.join(map(str, individual_author))

           family_names = re.findall("(?:[A-Z][A-Za-z'`-]+,)" , individual_author_string, flags=re.DOTALL)
           family_names = [w.replace(',', '') for w in family_names]
           return family_names 

def get_bibtex_given_names(individual_citation):
    author = re.findall(
            '(?<=author\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    if author:
           author_string = ' '.join(map(str, author))
           individual_author = re.findall("(?:[A-Z][A-Za-z'`-]+,)" + "\\s[A-Z][A-Za-z'`-]+" , author_string, flags=re.DOTALL)
           individual_author_string = ' '.join(map(str, individual_author))

           given_names =re.findall("(,\\s[A-Z][A-Za-z'`-]+)" , individual_author_string, flags=re.DOTALL)
           given_names = [w.replace(', ', '') for w in given_names]

           return given_names

def get_bibtex_year(individual_citation):
    year = re.findall(
            '(?<=year\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    if(bool(year)==False):
        year = re.findall(
            '(?<=year\\s=\\s)(.*?)(?=,)', individual_citation, flags=re.DOTALL)
    if year:
        year = ''.join(map(str, year))
        return year

def get_bibtex_title(individual_citation):
     title = re.findall(
            '(?<=title\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
     
     title = ''.join(map(str, title))
     return title

def get_bibtex_publisher(individual_citation):
    publisher = re.findall(
            '(?<=publisher\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    if (bool(publisher)==False):
        publisher = re.findall(
            '(?<=publisher\\s=\\s\{)(.*?)(?=\{)', individual_citation, flags=re.DOTALL)
    
    publisher = ''.join(map(str, publisher))
    return publisher


def get_bibtex_doi(individual_citation):
     doi = re.findall(
            '(?<=doi\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
     doi = ''.join(map(str, doi))
     return doi



def get_bibtex_url(individual_citation):
     url = re.findall(
            '(?<=URL\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    
     if (bool(url) == False):
         url = re.findall(
            '(?<=url\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
     return url

def get_bibtex_journal(individual_citation):
    journal = re.findall(
            '(?<=journal\\s=\\s\{)(.*?)(?=\},)', individual_citation, flags=re.DOTALL)
    return journal






        


