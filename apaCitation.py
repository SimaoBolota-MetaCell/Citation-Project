from htmlScraper import *
import re

doi_pattern = '(?:doi.org/)(.*?)(?=\,)'
authors = "(?:[A-Z][A-Za-z'`-]+)" + ", " + "(?:\w\.)"
year_num = '\(([0-9]{4})\)'

def get_apa_citations(link):
    soup = get_html(link )


    paragraphs = soup.find_all("p", {'dir': 'auto'})
    paragraphs = str(paragraphs)

    lists = soup.find_all("li")
    lists = str(lists)

    print(paragraphs)

    p_text_w_citation = re.findall(doi_pattern, paragraphs, flags=re.DOTALL)
    l_text_w_citation = re.findall(doi_pattern, lists, flags=re.DOTALL)

    print(bool(p_text_w_citation))

    if(bool(p_text_w_citation)):
        APA_text = strip_tags(paragraphs)
    elif(bool(l_text_w_citation)):
        APA_text = strip_tags(lists) 

    APA_text = APA_text.replace("\xa0", " ") 
    APA_text = re.sub('\.\\s\w\.', '.', APA_text)

    all_apa_authors = re.findall(authors, APA_text, flags=re.DOTALL)
    all_apa_authors = ', '.join(all_apa_authors)

    apa_pattern_wo_authors = year_num + "(.*?)" + doi_pattern

    all_apa_citations = re.findall(
    apa_pattern_wo_authors, APA_text, flags=re.DOTALL)

    return APA_text, all_apa_authors, all_apa_citations



def get_apa_family_names(all_apa_authors):
    
    apa_citation_family_names = re.findall(
        "(?:[A-Z][A-Za-z'`-]+,)", all_apa_authors, flags=re.DOTALL)
    apa_citation_family_names = [w.replace(',', '') for w in apa_citation_family_names]
    return apa_citation_family_names


def get_apa_given_names(all_apa_authors):
   
    apa_citation_given_names = re.findall(
        "(\,\\s[A-Z]\.)", all_apa_authors, flags=re.DOTALL)
    apa_citation_given_names = [w.replace(', ', '') for w in apa_citation_given_names]
    return apa_citation_given_names


def get_apa_year(individual_citation):

    apa_citation_year = re.findall('(\\s[0-9]{4}\.)', individual_citation, flags=re.DOTALL)
    apa_citation_year = [w.replace('.', '') for w in apa_citation_year]
    apa_citation_year = [w.replace(' ', '') for w in apa_citation_year]
    apa_citation_year = ''.join(map(str, apa_citation_year))
    return apa_citation_year

def get_apa_title(individual_citation):

    apa_citation_title = re.findall(
        '(?:[0-9]{4}\.\\s)([A-Z].*?)(?=\.)', individual_citation, flags=re.DOTALL)

    apa_citation_title = ' '.join(map(str, apa_citation_title))

    return apa_citation_title



def get_apa_journal(apa_citation_title, APA_text):
    apa_citation_journal = re.findall(apa_citation_title +'.'+ '(.*?)(?:doi)', APA_text, flags=re.DOTALL)
    return apa_citation_journal


def get_apa_doi(APA_text):
    apa_citation_doi = re.findall(doi_pattern, APA_text, flags=re.DOTALL)
    return apa_citation_doi




