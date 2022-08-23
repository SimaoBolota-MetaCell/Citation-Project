
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
import yaml
import git
import requests
import json

repo = git.Repo('/Users/simaosa/Desktop/MetaCell/Projects/CZI/Citation project/Citation-Project') 
origin = repo.remote("origin")  

assert origin.exists()
origin.fetch()

branch_name = 'Citation-branch14'

new_branch = repo.create_head(branch_name, origin.refs.main)  # replace prod with master/ main/ whatever you named your main branch
new_branch.checkout()


# takes url input and stores HTML of page
# html = requests.get( 'https://github.com/juglab/PlatyMatch/blob/master/README.md').text
# html = requests.get( 'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README.md').text
html = requests.get(
    'https://github.com/SimaoBolota-MetaCell/Citation-Project/blob/main/README2.md').text


soup = BeautifulSoup(html, 'html5lib')


snippets = soup.find_all("div", {
                         'class': 'highlight highlight-text-bibtex notranslate position-relative overflow-auto'})
snippets = str(snippets)


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
           family_names = [w.replace(',', '') for w in family_names]


           given_names =re.findall("(,\\s[A-Z][A-Za-z'`-]+)" , individual_author_string, flags=re.DOTALL)
           given_names = [w.replace(', ', '') for w in given_names]


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

        title = ''.join(map(str, title))
        publisher = ''.join(map(str, publisher))
        year = ''.join(map(str, year))
        doi = ''.join(map(str, doi))


        dict_file = {'cff-version': '1.2.0',
                     'message': 'If you use this plugin, please cite it using these metadata',
                     'authors': [{'family-names': family_names[0], 'given-names': given_names[0]}],
                     'title': title,
                     'references' : [{'title': publisher,'year':year, 'journal': journal}],
                     'doi': doi,
                     'date-released': year + '-01-01',
                     'identifiers': [{'type': 'url','value':url, 'description': ''}]}

        with open(r'./Citation-Project/CITATION.cff', 'w') as file:
            documents = yaml.dump(dict_file, file, sort_keys = False)




repo.index.add('CITATION.cff') 
repo.index.commit("BibTex Citation Added")
repo.git.push("--set-upstream", origin, repo.head.ref)



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


