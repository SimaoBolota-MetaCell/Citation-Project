
from bibtexCitation import *
from apaCitation import *
from bibtex_from_doi import *
import yaml



README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/onlyDOI.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/APA.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/bibtextandAPA.md'

if (bool(get_bibtex_citations(README_LINK))):
        all_bibtex_citations = get_bibtex_citations(README_LINK)
        print('BIBTEX CITATION')

        for individual_citation in all_bibtex_citations:

                individual_citation = re.sub('"', '}', individual_citation)
                individual_citation = re.sub('= }', '= {', individual_citation)

                citation_family_names = get_bibtex_family_names(individual_citation)
                citation_given_names = get_bibtex_given_names(individual_citation)
                citation_title = get_bibtex_title(individual_citation)
                citation_year = get_bibtex_year(individual_citation)
                citation_publisher = get_bibtex_publisher(individual_citation)
                citation_journal = get_bibtex_journal(individual_citation)
                citation_url = get_bibtex_url(individual_citation)
                citation_doi = get_bibtex_doi(individual_citation)

                print(citation_family_names)
                print('\n')
                print(citation_given_names)
                print('\n')
                print(citation_title)
                print('\n')
                print(citation_year)
                print('\n')
                print(citation_url)
                print('\n')
                print(citation_publisher)
                print('\n')
                print(citation_doi)
                print('\n')
                print(citation_journal)

elif(bool(get_apa_citations(README_LINK))):
        print('APA CITATION')

        APA_text, all_apa_authors, all_apa_citations = get_apa_citations(README_LINK)

        for individual_citation in all_apa_citations:
                print(individual_citation)

                individual_citation = ''.join(map(str, individual_citation))
                individual_citation = re.sub('\(', '', individual_citation)
                individual_citation = all_apa_authors + ' ' + individual_citation

                citation_family_names = get_apa_family_names(all_apa_authors)
                citation_given_names = get_apa_given_names(all_apa_authors)
                citation_year = get_apa_year(individual_citation)
                citation_year = citation_year + '-01-01'
                citation_title = get_apa_title(individual_citation)
                citation_journal = get_apa_journal(citation_title, APA_text)
                citation_doi = get_apa_doi(APA_text)

                print(citation_family_names)
                print('\n')
                print(citation_given_names)
                print('\n')
                print(citation_title)
                print('\n')
                print(citation_year)
                print('\n')
                print(citation_doi)
                print('\n')
                print(citation_journal)

else: # CHANGE THIS, going to APA instead of going to this logic
        all_bibtex_citations = get_citation_from_doi(README_LINK)   
        print('DOI CITATION')  
        for individual_citation in all_bibtex_citations:
                print(individual_citation)
                individual_citation = re.sub('"', '}', individual_citation)
                individual_citation = re.sub('= }', '= {', individual_citation)

                citation_family_names = get_bibtex_family_names(individual_citation)
                citation_given_names = get_bibtex_given_names(individual_citation)
                citation_title = get_bibtex_title(individual_citation)
                citation_year = get_bibtex_year(individual_citation)
                citation_publisher = get_bibtex_publisher(individual_citation)
                citation_journal = get_bibtex_journal(individual_citation)
                citation_url = get_bibtex_url(individual_citation)
                citation_doi = get_bibtex_doi(individual_citation)

                print(citation_family_names)
                print('\n')
                print(citation_given_names)
                print('\n')
                print(citation_title)
                print('\n')
                print(citation_year)
                print('\n')
                print(citation_url)
                print('\n')
                print(citation_publisher)
                print('\n')
                print(citation_doi)
                print('\n')
                print(citation_journal)



dict_file = {'cff-version': '1.2.0',
                     'message': 'If you use this plugin, please cite it using these metadata',
                     'title': citation_title,
                     'references' : [{'title': 'hi','year':citation_year, 'journal': citation_journal}],
                     'doi': citation_doi,
                     'date-released': citation_year,
                     'identifiers': [{'type': 'hi','value':citation_url, 'description': ''}],
                     'references' : [{'type':'book', 'publisher':[{'name':citation_publisher}]}]}


for i in range(len(citation_family_names)):
    
    author_dict_file = {'authors': [{'family-names': citation_family_names[i], 'given-names': citation_given_names[i]}],}
    
    for key, value in author_dict_file.items():
     if key in dict_file:
        dict_file[key].extend(value)
     else:
        dict_file[key] = value
print(dict_file)

with open(r'./Citation-Project/CITATION.cff', 'w') as file:
            documents = yaml.dump(dict_file, file, sort_keys = False)

