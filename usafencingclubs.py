import pandas as pd
from bs4 import BeautifulSoup
import requests

page_number = 1
all_clubs = []
html_request = requests.get('https://member.usfencing.org/clubs?page=' + str(page_number))

while html_request.status_code == 200:

    try:
        soup = BeautifulSoup(html_request.text, features='html.parser')
        club_table = soup.find('tbody').find_all('tr')
    except:
        break

    for i in range(len(club_table)):
    #for i in range(1):
        id = ''
        expiry = ''
        address = ''
        number = ''
        email = ''
        website = ''

        # collect club data
        name = club_table[i].p.get_text()
        if club_table[i].find('p').findNext('p').get_text().strip() == 'Pending Renewal':
            id = club_table[i].find('p').findNext('p').findNext('p').get_text().split(',', 1)[0]
            expiry = club_table[i].find('p').findNext('p').findNext('p').get_text().split(',', 1)[1].strip()
        else:
            id = club_table[i].find('p').findNext('p').get_text().split(',', 1)[0]
            expiry = club_table[i].find('p').findNext('p').get_text().split(',', 1)[1].strip()

        # this column changes so we need to validate which item we are grabbing
        p_tag_1 = club_table[i].find('td').findNext('td').find('p').get_text().strip()
        p_tag_2 = club_table[i].find('td').findNext('td').find('p').findNext('p').get_text()
        try:
            p_tag_3 = club_table[i].find('td').findNext('td').find('p').findNext('p').findNext('p').get_text()
        except:
            p_tag_3 = ''
        try:
            p_tag_4 = club_table[i].find('td').findNext('td').find('p').findNext('p').findNext('p').findNext('p').get_text()
        except:
            p_tag_4 = ''

        p_tags = [p_tag_1, p_tag_2, p_tag_3, p_tag_4]
        
        for p_tag in p_tags:
            if ',' in p_tag:
                address = p_tag
            elif p_tag.startswith('('):
                number = p_tag
            elif '@' in p_tag:
                email = p_tag
            elif '.' in p_tag:
                website = p_tag
        
        region = club_table[i].find('td').findNext('td').find('p').findNext('td').get_text().strip()
        division = club_table[i].find('td').findNext('td').find('p').findNext('td').findNext('td').get_text().strip()


        """
        # niave approach
        address = club_table[i].find('p', {'itemprop': 'address'}).get_text().strip()
        number = club_table[i].find('p', {'itemprop': 'address'}).findNext('p').get_text()
        email = club_table[i].find('p', {'itemprop': 'address'}).findNext('p').findNext('p').get_text()
        website = club_table[i].find('p', {'itemprop': 'address'}).findNext('p').findNext('p').findNext('p').get_text()
        """

        # add to the list of clubs
        new_club = [id, name, address, number, email, website, expiry, region, division]
        all_clubs.append(new_club)
        
    # setup next page
    print('page number: ', page_number)
    page_number += 1
    html_request = requests.get('https://member.usfencing.org/clubs?page=' + str(page_number))


#save data
#print(all_clubs)
clubs_df = pd.DataFrame(all_clubs)
clubs_df.columns = ['ID', 'Club Name', 'Address', 'Phone Number', 'Email', 'Website', 'Expiry', 'Region', 'Division']
clubs_df.set_index('ID', inplace=True)
clubs_df.to_csv('./all_clubs.csv')