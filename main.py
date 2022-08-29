
#########################  IMPORTS  ##########################

from bibtexCitation import *
from apaCitation import *
from bibtex_from_doi import *
import yaml
import git


# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/onlyDOI.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/APA.md'
README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/bibtextandAPA.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/emptyreadme.md'


NOT_AVAILABLE = ['Not Available']


citation_title = {}
citation_publisher = {}
citation_url = {}
citation_family_names = {}
citation_give_names = {}
citation_year = {}
citation_journal = {}
citation_doi = {}
#########################  CREATE BRANCH  ##########################


repo = git.Repo(
    '/Users/simaosa/Desktop/MetaCell/Projects/CZI/Citation project/Citation-Project')
origin = repo.remote("origin")
assert origin.exists()
origin.fetch()

#########################  BIBTEX CITATION  ##########################

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


#########################  APA CITATION  ##########################


elif (bool(get_apa_citations(README_LINK))):

    APA_text, all_apa_authors, all_apa_citations = get_apa_citations(
        README_LINK)

    if (bool(all_apa_authors)):

        print('APA CITATION')

        APA_text, all_apa_authors, all_apa_citations = get_apa_citations(
            README_LINK)

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


#########################  ONLY DOI  ##########################
elif (bool(get_citation_from_doi(README_LINK))):
    print('DOI CITATION')
    all_bibtex_citations = get_citation_from_doi(README_LINK)
    print('DOI CITATION')
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


#################### No CITATION INFO - USE GIT AUTHOR INFO ####################

elif (bool(get_citation_from_doi(README_LINK)) == False):
    GIT_FAMILY_NAMES_PATTERN = '(?<=Author:\\s)(.*?)(?=\\s)'

    print('NO CITATION INFO')
    git_author = repo.git.show("-s", "--format=Author: %an <%ae>")

    citation_given_names = re.findall(
        GIT_FAMILY_NAMES_PATTERN, git_author, flags=re.DOTALL)
    citation_given_names_string = ''.join(map(str, citation_given_names))

    GIT_GIVEN_NAMES_PATTERN = '(?<=Author:\\s%s\\s)(.*?)(?=\\s)' % citation_given_names_string

    citation_family_names = re.findall(
        GIT_GIVEN_NAMES_PATTERN, git_author, flags=re.DOTALL)


#########################  DICT FILE  ##########################

dict_file = {'cff-version': '1.2.0',
             'message': 'If you use this plugin, please cite it using these metadata',
             'references':[{'type':'software', }],
             }

######
if (bool(citation_family_names) and citation_family_names != NOT_AVAILABLE):
    for i in range(len(citation_family_names)):
        author_dict_file = {'authors': [
            {'family-names': citation_family_names[i], 'given-names': citation_given_names[i]}], }

elif (bool(citation_family_names) == False):
    citation_family_names = NOT_AVAILABLE
    citation_family_names = ''.join(map(str, citation_family_names))
    citation_given_names = NOT_AVAILABLE
    citation_given_names = ''.join(map(str, citation_given_names))
    author_dict_file = {[{'authors': [
        {'family-names': citation_family_names, 'given-names': citation_given_names}], }]}

for key, value in author_dict_file.items():
    if key in dict_file:
        dict_file[key].extend(value)
    else:
        dict_file[key] = value

######
if (bool(citation_title) and citation_title != NOT_AVAILABLE):
    for i in range(len(citation_title)):
        title_dict_file = {'title': citation_title}
elif (bool(citation_title) == False):
    citation_title = NOT_AVAILABLE
    citation_title = ''.join(map(str, citation_title))
    title_dict_file = {'title': citation_title}
for key, value in title_dict_file.items():
    if key in dict_file:
        dict_file[key].extend(value)
    else:
        dict_file[key] = value

######
if (bool(citation_year) and citation_year != NOT_AVAILABLE):
    for i in range(len(citation_year)):

        year_dict_file = {'date-released': citation_year + '-01-01'}
elif (bool(citation_year) == False):
    citation_year = NOT_AVAILABLE
    citation_year = ''.join(map(str, citation_year))

    year_dict_file = {'date-released': citation_year}

for key, value in year_dict_file.items():
    if key in dict_file:
        dict_file[key].extend(value)
    else:
        dict_file[key] = value

######
if (bool(citation_url) and citation_url != NOT_AVAILABLE):
    for i in range(len(citation_url)):
        citation_url = ''.join(map(str, citation_url))
        url_dict_file = {'url': citation_url}
elif(bool(citation_url) == False):
        citation_url = NOT_AVAILABLE
        citation_url = ''.join(map(str, citation_url))
        url_dict_file = {'url': citation_url}
for key, value in url_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value

######
if (bool(citation_doi) and citation_doi != NOT_AVAILABLE):
    for i in range(len(citation_doi)):
        citation_doi = ''.join(map(str, citation_doi))
        doi_dict_file = {'doi': citation_doi}
elif(bool(citation_doi) == False):
        citation_doi = NOT_AVAILABLE
        citation_doi = ''.join(map(str, citation_doi))
        doi_dict_file = {'doi': citation_doi}
for key, value in doi_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value

######
if (bool(citation_publisher) and citation_publisher != NOT_AVAILABLE):
    for i in range(len(citation_publisher)):
        publisher_dict_file = {'references': [
            {'type': 'book', 'publisher': citation_publisher}]}

elif(bool(citation_publisher) == False):
        citation_publisher = NOT_AVAILABLE
        citation_publisher = ''.join(map(str, citation_publisher))
        publisher_dict_file = {'references': [
            {'type': 'book', 'publisher': citation_publisher}]}
for key, value in publisher_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value

######
if (bool(citation_journal) and citation_journal != NOT_AVAILABLE):
    for i in range(len(citation_journal)):
        citation_journal = ''.join(map(str, citation_journal))
        journal_dict_file = {'references': [
            {'type': 'article', 'journal': citation_journal}]}
elif (bool(citation_journal) == False):
        citation_journal = NOT_AVAILABLE
        citation_journal = ''.join(map(str, citation_journal))
        journal_dict_file = {'references': [
            {'type': 'article', 'journal': citation_journal}]}

for key, value in journal_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value


print('\n')
print(dict_file)
with open(r'./Citation-Project/CITATION.cff', 'w') as file:
    documents = yaml.dump(dict_file, file, sort_keys=False)


#########################  PUSH COMMITS and PULL REQUEST  ##########################


# repo.index.add('CITATION.cff')
# repo.index.commit("BibTex Citation Added")
# repo.git.push("--set-upstream", origin, repo.head.ref)


# def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
#     """Creates the pull request for the head_branch against the base_branch"""
#     git_pulls_api = "https://github.com/api/v3/repos/{0}/{1}/pulls".format(
#         project_name,
#         repo_name)
#     headers = {
#         "Authorization": "token {0}".format(git_token),
#         "Content-Type": "application/json"}

#     payload = {
#         "title": title,
#         "body": description,
#         "head": head_branch,
#         "base": base_branch,
#     }

#     r = requests.post(
#         git_pulls_api,
#         headers=headers,
#         data=json.dumps(payload))

#     if not r.ok:
#         print("Request Failed: {0}".format(r.text))

# create_pull_request(
#     "<your_project>", # project_name
#     "Citation-Project", # repo_name
#     "My pull request title", # title
#     "My pull request description", # description
#     branch_name, # head_branch
#     "main", # base_branch
#     "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", # git_token
# )
