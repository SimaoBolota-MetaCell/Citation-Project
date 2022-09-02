from htmlScraper import *
import re

APA_DOI_PATTERN = '(?:doi.org/)(.*?)(?=\,)'
APA_AUTHORS_PATTERN = "(?:[A-Z][A-Za-z'`-]+)" + ", " + "(?:\w\.)"
APA_YEAR_NUM_PATTERN = '\(([0-9]{4})\)'
APA_FULL_DOI_PATTERN = '(10.(\d)+/([^(\s\>\"\<)])+)'
APA_FAMILY_NAME_PATTERN = "(?:[A-Z][A-Za-z'`-]+,)"
APA_GIVEN_NAME_PATTERN = "(\,\\s[A-Z]\.)"
APA_TITLE_PATTERN = '(?:[0-9]{4}\.\\s)([A-Z].*?)(?=\.)'
APA_YEAR_PATTERN = '(\\s[0-9]{4}\.)'





def get_apa_citations(link):
    soup = get_html(link )

    paragraphs = soup.find_all("p", {'dir': 'auto'})
    paragraphs = str(paragraphs)

    lists = soup.find_all("li")
    lists = str(lists)

    p_text_w_citation = re.findall(APA_FULL_DOI_PATTERN, paragraphs, flags=re.DOTALL)
    l_text_w_citation = re.findall(APA_FULL_DOI_PATTERN, lists, flags=re.DOTALL)

    if(bool(p_text_w_citation)):
        APA_text = strip_tags(paragraphs)
    elif(bool(l_text_w_citation)):
        APA_text = strip_tags(lists) 
    else:
        APA_text = False

    if(bool(APA_text)):
        APA_text = APA_text.replace("\xa0", " ") 
        APA_text = re.sub('\.\\s\w\.', '.', APA_text)

        all_apa_authors = re.findall(APA_AUTHORS_PATTERN, APA_text, flags=re.DOTALL)
        all_apa_authors = ', '.join(all_apa_authors)

        apa_pattern_wo_authors = APA_YEAR_NUM_PATTERN + "(.*?)" + APA_DOI_PATTERN

        all_apa_citations = re.findall(
        apa_pattern_wo_authors, APA_text, flags=re.DOTALL)

        return APA_text, all_apa_authors, all_apa_citations



def get_apa_family_names(all_apa_authors):
    
    apa_citation_family_names = re.findall(
        APA_FAMILY_NAME_PATTERN, all_apa_authors, flags=re.DOTALL)
    apa_citation_family_names = [w.replace(',', '') for w in apa_citation_family_names]
    return apa_citation_family_names


def get_apa_given_names(all_apa_authors):
   
    apa_citation_given_names = re.findall(
        APA_GIVEN_NAME_PATTERN, all_apa_authors, flags=re.DOTALL)
    apa_citation_given_names = [w.replace(', ', '') for w in apa_citation_given_names]
    return apa_citation_given_names


def get_apa_year(individual_citation):

    apa_citation_year = re.findall(APA_YEAR_PATTERN, individual_citation, flags=re.DOTALL)
    apa_citation_year = [w.replace('.', '') for w in apa_citation_year]
    apa_citation_year = [w.replace(' ', '') for w in apa_citation_year]
    apa_citation_year = ''.join(map(str, apa_citation_year))
    return apa_citation_year

def get_apa_title(individual_citation):

    apa_citation_title = re.findall(
        APA_TITLE_PATTERN, individual_citation, flags=re.DOTALL)

    apa_citation_title = ' '.join(map(str, apa_citation_title))

    return apa_citation_title


def get_apa_journal(apa_citation_title, APA_text):
    apa_citation_journal = re.findall(apa_citation_title +'.'+ '(.*?)(?:doi)', APA_text, flags=re.DOTALL)
    return apa_citation_journal


def get_apa_doi(APA_text):
    apa_citation_doi = re.findall(APA_DOI_PATTERN, APA_text, flags=re.DOTALL)
    return apa_citation_doi




