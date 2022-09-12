
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

Question 1.1: Do we want to show the subcomponents if they are not available/found? Or do we only create the .CFF with the components that have meaningful information

Question 1.2: If we want to show them, and since some of the subcomponents might not be found/available (in the example, the 'None' and '[] ), should they be displayed as an empty string ' ' or as 'Not Available'?


For when No Citation Information is found in the README.md,
- console warning

![image](https://user-images.githubusercontent.com/99416933/189680046-21508a07-7d2e-443e-aa2c-e1072fcfa9a5.png)

- pop up warning 

![image](https://user-images.githubusercontent.com/99416933/189680547-aecfca8c-64c3-4468-a2f7-76870a5da0cf.png)


and then the .CFF is created taking in **only the GitHub Repo Author name** as the Author:

![Screenshot at Aug 29 15-40-11](https://user-images.githubusercontent.com/99416933/187227630-8f0960d6-f12d-4d2e-9f02-cdb31ece9260.png)

**DICT FILE**:


Question 1: Do we want the main citation in CFF format to be for the software or the paper/article it's based on?

Creating a CFF has different keys for the different type of citation. For ```type: article``` information about the publication like the journal is also a key

<img width="810" alt="Screenshot_at_Aug_25_15-33-20" src="https://user-images.githubusercontent.com/99416933/187229511-9a02cd9d-1df5-41f5-bd08-9caf4485e345.png">

while for ```type:software``` it doesn't

<img width="616" alt="Screenshot_at_Aug_25_15-36-24" src="https://user-images.githubusercontent.com/99416933/187229564-cec05a59-004d-49b4-9a9e-ff5a99ab1a6c.png">

Solution: I can put it as both when the journal variable is not empty 

<img width="827" alt="Screenshot_at_Aug_25_15-35-54" src="https://user-images.githubusercontent.com/99416933/187229604-ab20dc8f-0f33-4f88-8369-5510bc7a585d.png">

**CFF format updated for journal/book references**:

As proposed, have the main citation referencing the software and add sub-reference type article/book if the variables holding the publisher name or journal name are not empty

Another thing added was to add the doi key and value as a type article/book reference (if variable journal exists DOI is added as article, if variable publisher exists DOI is added as book, if it doesn't found any journal name or publisher name DOI is added as type article by default), so it doesn't appear in the main software citation but in the article/book sub reference


![image](https://user-images.githubusercontent.com/99416933/189682177-4930f732-ee98-477c-92b2-b33b4f192737.png)




**Git Automations**:

- Create Branch (unique names)
- Push Commit (pushes only the CITAION.CFF)
- Pull Request (requires git token, requested as input when you run the code)

![image](https://user-images.githubusercontent.com/99416933/189687633-462cedc9-fb22-4023-909c-55b674becb85.png)

<img width="1345" alt="image" src="https://user-images.githubusercontent.com/99416933/189687912-2e5ce443-853d-43f4-8d61-60483ff3da65.png">



**Unit tests** (just run pytest):

- Test for APA method
- Test for Bibtex method
- Test for only DOI method

![image](https://user-images.githubusercontent.com/99416933/189692401-35a56d51-ae93-4225-a196-acd825453360.png)


Asserting that the variables that hold the citation information exist and match with a specific example
&
Creating a test dict form an example (contents for the CITATION.CFF) and compare it with that set example supposed outcome.

Example:

![image](https://user-images.githubusercontent.com/99416933/189691504-329190bf-8659-414d-9b0e-b38e01c4c47b.png)




**PROCESS**:

1. BibTex Citation
2. APA Citation
3. DOI only Citation
4. No Citation info

