
#########################  IMPORTS  ##########################

from bibtexCitation import *
from apaCitation import *
from bibtex_from_doi import *
from create_dict import *
import yaml
import git
import json
import warnings


# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/onlyDOI.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/APA.md'
# README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/bibtextandAPA.md'
README_LINK = 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/emptyreadme.md'


citation_title = {}
citation_publisher = {}
citation_url = {}
citation_family_names = {}
citation_give_names = {}
citation_year = {}
citation_journal = {}
citation_doi = {}

isBibtex = bool(get_bibtex_citations(README_LINK))
isDOI = bool(get_citation_from_doi(README_LINK))


GIT_FAMILY_NAMES_PATTERN = '(?<=Author:\\s)(.*?)(?=\\s)'


#########################  CREATE BRANCH  ##########################


repo = git.Repo(
    '/Users/simaosa/Desktop/MetaCell/Projects/CZI/Citation project/Citation-Project')
origin = repo.remote("origin")
assert origin.exists()
origin.fetch()

repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]

git_author = repo.git.show("-s", "--format=Author: %an <%ae>")


# branch_name = 'TestBranch-1Sep2022x1'
# new_branch = repo.create_head(branch_name, origin.refs.main) 
# new_branch.checkout()

#########################  BIBTEX CITATION  ##########################

if (isBibtex):
    print('BibTex Citation')
    all_bibtex_citations = get_bibtex_citations(README_LINK)
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


    filedict = add_to_dict(citation_family_names, citation_given_names, citation_title, citation_year, citation_url, citation_doi, citation_publisher, citation_journal )

    print('\n')
    print(filedict)
    print('\n')
    with open(r'./Citation-Project/CITATION.cff', 'w') as file:
            documents = yaml.dump(filedict, file, sort_keys=False)


#########################  APA CITATION  ##########################


elif isBibtex==False and bool(get_apa_citations(README_LINK)):
    
    
    APA_text, all_apa_authors, all_apa_citations = get_apa_citations(
        README_LINK)

    if (bool(all_apa_authors)):
        print('APA Citation')
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


        filedict = add_to_dict(citation_family_names, citation_given_names, citation_title, citation_year, citation_url, citation_doi, citation_publisher, citation_journal )

        print('\n')
        print(filedict)
        print('\n')
        with open(r'./Citation-Project/CITATION.cff', 'w') as file:
                documents = yaml.dump(filedict, file, sort_keys=False)

#########################  ONLY DOI  ##########################

    else:
        print('DOI Citation')
        all_bibtex_citations = get_citation_from_doi(README_LINK)
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


        filedict = add_to_dict(citation_family_names, citation_given_names, citation_title, citation_year, citation_url, citation_doi, citation_publisher, citation_journal )

        print('\n')
        print(filedict)
        print('\n')
        with open(r'./Citation-Project/CITATION.cff', 'w') as file:
                documents = yaml.dump(filedict, file, sort_keys=False)


#################### No CITATION INFO - USE GIT AUTHOR INFO ####################

else:
    print('\n')
    warnings.warn("Warning...........Please insert citation or DOI ")

    
    citation_given_names = re.findall(
        GIT_FAMILY_NAMES_PATTERN, git_author, flags=re.DOTALL)
    citation_given_names_string = ''.join(map(str, citation_given_names))

    GIT_GIVEN_NAMES_PATTERN = '(?<=Author:\\s%s\\s)(.*?)(?=\\s)' % citation_given_names_string

    citation_family_names = re.findall(
        GIT_GIVEN_NAMES_PATTERN, git_author, flags=re.DOTALL)

    filedict = add_to_dict(citation_family_names, citation_given_names, citation_title, citation_year, citation_url, citation_doi, citation_publisher, citation_journal )

    print('\n')
    print(filedict)
    print('\n')
    with open(r'./Citation-Project/CITATION.cff', 'w') as file:
            documents = yaml.dump(filedict, file, sort_keys=False)




#########################  PUSH COMMITS and PULL REQUEST  ##########################


# repo.index.add('CITATION.cff')
# repo.index.commit("BibTex Citation Added")
# repo.git.push("--set-upstream", origin, repo.head.ref)


# def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
#     """Creates the pull request for the head_branch against the base_branch"""
#     git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
#         project_name,
#         repo_name)
#     headers = {
#         "Authorization": "token {0}".format(git_token),
#         "Content-Type": "application/vnd.github+json"}

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
#     "Simão Sá", # owner_name
#     repo_name, # repo_name
#     "My pull request title", # title
#     "My pull request description", # description
#     branch_name, # head_branch
#     "main", # base_branch
#     "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", # git_token
# )
