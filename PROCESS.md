
Taking a README URL, **perform a request to the webpage in order to get its html** information

<img width="590" alt="html" src="https://user-images.githubusercontent.com/99416933/184635095-ad07556c-96fa-46fa-abb6-15edd181f6f6.png">


You are able to **differentiate the types of citations by the tags** used:
- for BibTex citations -> ```div, {class: highlight highlight-text-bibtex notranslate position-relative overflow-auto})```  <img width="585" alt="Screenshot at Aug 15 13-31-45" src="https://user-images.githubusercontent.com/99416933/184635571-75675458-360d-4dad-8a16-18b9427d3dec.png">

- for APA citations -> simple p tags, since they are displayed as normal text<img width="579" alt="ptags" src="https://user-images.githubusercontent.com/99416933/184635606-4633184b-4e23-451e-af69-99b00ce3d69b.png">


Since all HTML text is retrived, by **stripping the HTML tags**, we get only the relevant text

- APA Citations <img width="586" alt="Screenshot at Aug 15 13-34-15" src="https://user-images.githubusercontent.com/99416933/184636196-04f7e88d-ed97-421d-9b9a-e51aee55fdf5.png">

- Bibtex Citations <img width="586" alt="Screenshot at Aug 15 13-37-55" src="https://user-images.githubusercontent.com/99416933/184636294-0ccc696a-780a-4b2d-ab0f-9c438a61b925.png">


At the moment, eventhough the data displayed is the correct one, there are text elements contained in APA citations and Bibtext Citations that are not part of the citation.
For this reason, the next step is to **create a pattern using regular expressions, so only the correct formatted citations and information are displayed**
- BibTex: <img width="602" alt="Screenshot at Aug 15 13-39-40" src="https://user-images.githubusercontent.com/99416933/184636584-b664b487-094b-4763-85d6-120b28e796b5.png">

- APA: ![Screenshot at Aug 22 16-16-18](https://user-images.githubusercontent.com/99416933/185956927-3c1f8467-0818-4dd3-a9c5-9b160d8bd29e.png)



After having all the correct citations, **parse them into its subcomponents** (when applicable):
- BibTex (author, doi, year, journal, url, publisher)
  - example 1:![Screenshot at Aug 22 16-01-49](https://user-images.githubusercontent.com/99416933/185954227-b0786bec-ae29-4072-827f-84371f6e2b2c.png)

  - example 2:![Screenshot at Aug 22 16-03-23](https://user-images.githubusercontent.com/99416933/185954245-17ae7ba9-8852-42ec-ae42-327ec1117498.png)

- APA (author, doi, year, journal, url, publisher)
  - example :![Screenshot at Aug 22 16-12-56](https://user-images.githubusercontent.com/99416933/185956227-a2034225-e0a0-491c-8cfe-16e69fe6aca0.png)

So far there is logic implemented to take in account BibTex and APA Citations from the README.md and retrieve its subcomponents. For when no APA or BibTex Citation is found in the README.md, a **DOI Scraper** looks for a DOI pattern in the README.md and using a DOI Content Negotioation (http://crosscite.org/cn/) the string with the bibtex entry is retrived:

![Screenshot at Aug 29 15-25-50](https://user-images.githubusercontent.com/99416933/187224446-d6bf4d2b-d585-4200-90b9-826d87fd9397.png)


Since the bibtex patterns were previously implemented in the BibTex Citation code, they are used again to retrieve the subcomponents of the citation and create the .CFF

![Screenshot at Aug 29 15-34-13](https://user-images.githubusercontent.com/99416933/187226233-d8869e6e-89c4-4867-a08e-095b91608046.png)

Question: Since some of the subcomponents might not be found/available (in the example, the 'None' and '[] ), should they be displayed as an empty string ' ' or as 'Not Available'?

For when No Citation Information is found in the README.md, the .CFF is created taking in **only the GitHub Repo Author name**:

![Screenshot at Aug 29 15-40-11](https://user-images.githubusercontent.com/99416933/187227630-8f0960d6-f12d-4d2e-9f02-cdb31ece9260.png)
![Screenshot at Aug 29 15-40-35](https://user-images.githubusercontent.com/99416933/187227635-aa61d20e-3c29-4d45-a117-71e5be73e8b7.png)


**Git Automations**:

- Create Branch
- Push Commit
- Pull Request (TO DO)

**PROCESS**:

1. BibTex Citation
2. APA Citation
3. DOI only Citation
4. No Citation info


TODO:

Having the citations parsed into its subcomponents, **create the .CFF file** (PyYAML or PyCFF) storing the subcomponents into the corresponding CFF keys https://elib.dlr.de/147385/1/schema-guide.pdf.

Using a GitHub plugin or integration, **create a flow to submit a Pull request of the automatically generated .CFF.** The author can then review/edit/approve the citation and eventually merge if agreed.
This way the .CFF becomes part of the repo.

This is done to ensure that we are not direcly pushing a file into someone else's repo. Giving room for the Repo owner to add more infomration or correct information if needed and to double check the output of this Citation process.

