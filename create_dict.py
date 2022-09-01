import yaml


NOT_AVAILABLE = ['Not Available']







def add_to_dict(family_names, given_names, title, year, url, doi, publisher, journal ):


    dict_file = {'cff-version': '1.2.0',
             'message': 'If you use this plugin, please cite it using these metadata',
             }

    ######
    if (bool(title) and title != NOT_AVAILABLE):
        for i in range(len(title)):
            title_dict_file = {'title': title}
    elif (bool(title) == False):
        title_dict_file = {'title': NOT_AVAILABLE}
    for key, value in title_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value


     ######
    if (bool(doi) and doi != NOT_AVAILABLE):
        
            doi = ''.join(map(str, doi))
            doi_dict_file = {'doi': doi}
    elif(bool(doi) == False):
            doi_dict_file = {'doi': NOT_AVAILABLE}
    for key, value in doi_dict_file.items():
            if key in dict_file:
                dict_file[key].extend(value)
            else:
                dict_file[key] = value
   
    ######
    if (bool(family_names) and family_names != NOT_AVAILABLE):
        for i in range(len(family_names)):
            author_dict_file = {'authors': [
                {'family-names': family_names[i], 'given-names': given_names[i]}], }
            
            for key, value in author_dict_file.items():
                 if key in dict_file:
                    dict_file[key].extend(value)
                 else:
                    dict_file[key] = value

    elif (bool(family_names) == False):
        author_dict_file = {'authors': [{'family-names': 'Not Available', 'given-names': 'Not Available'}], }

        for key, value in author_dict_file.items():
            if key in dict_file:
                dict_file[key].extend(value)
            else:
                dict_file[key] = value

    

    ######
    if (bool(year) and year != NOT_AVAILABLE):
       

            year_dict_file = {'date-released': year + '-01-01'}
    elif (bool(year) == False):
        year_dict_file = {'date-released': NOT_AVAILABLE}

    for key, value in year_dict_file.items():
        if key in dict_file:
            dict_file[key].extend(value)
        else:
            dict_file[key] = value

    ######
    if (bool(url) and url != NOT_AVAILABLE):
        
            url = ''.join(map(str, url))
            url_dict_file = {'url': url}
    elif(bool(url) == False):
            url_dict_file = {'url': NOT_AVAILABLE}
    for key, value in url_dict_file.items():
            if key in dict_file:
                dict_file[key].extend(value)
            else:
                dict_file[key] = value

    ######
    if (bool(publisher) and publisher != NOT_AVAILABLE):

        if(bool(doi)):
            if(bool(title)):
                

                    publisher_dict_file = {'references': [
                        {'type': 'book','title':title, 'publisher': publisher,'doi':doi  }]}

                    for key, value in publisher_dict_file.items():
                        if key in dict_file:
                            dict_file[key].extend(value)
                        else:
                            dict_file[key] = value
            else:
                publisher_dict_file = {'references': [
                        {'type': 'book','title':'Not Available', 'publisher': publisher,'doi':doi  }]}
                
                for key, value in publisher_dict_file.items():
                    if key in dict_file:
                        dict_file[key].extend(value)
                    else:
                        dict_file[key] = value
        else:
            publisher_dict_file = {'references': [
                        {'type': 'book','title':'Not Available', 'publisher': publisher,'doi':'Not Available' }]}

            
            for key, value in publisher_dict_file.items():
                    if key in dict_file:
                        dict_file[key].extend(value)
                    else:
                        dict_file[key] = value

    ######
    if (bool(journal) and journal != NOT_AVAILABLE):
        
        journal = ''.join(map(str, journal))

        if(bool(doi)):
            if(bool(title)):

                    journal_dict_file = {'references': [
                        {'type': 'article','title':title, 'journal': journal,'doi': doi  }]}

                    for key, value in journal_dict_file.items():
                        if key in dict_file:
                            dict_file[key].extend(value)
                        else:
                            dict_file[key] = value
            else:

                    journal_dict_file = {'references': [
                        {'type': 'article','title':'Not Available', 'journal': journal,'doi': doi  }]}

                    for key, value in journal_dict_file.items():
                        if key in dict_file:
                            dict_file[key].extend(value)
                        else:
                            dict_file[key] = value
        else:
            journal_dict_file = {'references': [
                        {'type': 'article','title':'Not Available', 'journal': journal,'doi': 'Not Available'  }]}
   

            for key, value in journal_dict_file.items():
                    if key in dict_file:
                        dict_file[key].extend(value)
                    else:
                        dict_file[key] = value

    print('\n')
    print('Citation Dict File created')

    return dict_file
    