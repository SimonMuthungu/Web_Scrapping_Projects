# I created this script to scrape the jumia website mobile phones section
# It is to return and write the info it gets to a csv file so i can analyse the file and choose the phone i want to buy
# this is much better than me going phone by phone on their website!
# Lets do this...

import requests
from bs4 import BeautifulSoup as bs
from csv import writer

jumia_url = "https://www.jumia.co.ke/phones-tablets/" # the url we're scrapping

response = requests.get(jumia_url) 

if response:  # to be sure we got the response

    jumia_soup = bs(response.content, 'lxml')  

    list_of_phones = jumia_soup.find_all('div', class_="info")

    if list_of_phones:  # to escape tracebacks, and tell the user whether the scrapping process gave back content
        print('\nGarrit!\n')
    else:
        print('\nSorry, don garrit!. For some reason, your scraper returned empty content\n')


    with open('Jumia_phones.csv', 'w', encoding='utf8', newline='') as f: # to open the csv file 
        thewriter = writer(f)
        thewriter.writerow(['name', 'screen_size','memory_size', 'battery', 'price', 'old_price', 'pcnt_deduction', 'rating'])  # writing the headers
    
        for phone in list_of_phones: 

            name = phone.find('h3', class_='name').text

            name_alone = name.split(',')[0] # the names come as long text so i had to split them where there is a comma. Some items didnt have a comma

            try:
                inches = name.split(',')[1]
                memory_size = name.split(',')[2]
                battery = name.split(',')[3]
            except:
                inches = 'no screen size info'
                memory_size = 'No memory size info'
                battery = 'No battery info' 

            price = phone.find('div', class_='prc').text

            old_price = phone.find('div', class_='old').text

            pcnt_deduction = phone.find('div', class_='bdg').text

            if phone.find('div', class_='stars'): # some devices don have ratings thus this prevents errors...
                rating = phone.find('div', class_='stars').text
            else:
                rating = 'No rating on this one!'

            info = [name_alone, inches, memory_size, battery, price, old_price, pcnt_deduction, rating]

            thewriter.writerow(info) # writing row at a time after every iteration

        else:
            print('Sorry, there was no response. Maybe you could try again')

print('\nDone with writing. Thank you!\n') 
