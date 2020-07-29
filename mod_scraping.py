import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import numpy as np
import pandas as pd
from datetime import datetime
import csv

#To Display all columns of a pandas DataFrame (remax_data)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
proxies = {
    "http": 'http://110.74.222.159:40348',
    "https": 'http://181.118.167.104:80'
}

def main():
    print_header()
    pages = np.arange(0, 500, 10)
    for page in pages:
        url = "https://www.remax-quebec.com/fr/maison-a-vendre/montreal/resultats.rmx?offset=" + str(page) + "#listing"" + str(page) + "
        html = get_html_from_url(url, HEADERS, proxies)
        remax_data = get_data_from_html(html)
        add_data_to_file(remax_data)
        print(remax_data)
        sleep(randint(2, 10))

def print_header():
    print('---------------------------------')
    print('       Remax web Scraping ')
    print('---------------------------------')
    print()

def get_html_from_url(url, headers, proxies):
    response = requests.get(url, headers=headers, proxies=proxies).content
    # Parse the html content
    soup = BeautifulSoup(response, "html.parser")
    return soup

def get_data_from_html(html):
    #Chercher code ULS
    uls = list()
    property_uls = html.find_all("div", attrs={"class":"property-uls"})
    for prop_uls in property_uls:
        mots = prop_uls.get_text().split(":")
        mots = mots[1].split("\r")
        mots = mots[0].split(" ")
        uls.append(mots[1])

    #Chercher type
    type = list()
    property_type = html.find_all("h2", attrs={"class":"property-type"})
    for prop_type in property_type:
        mots = prop_type.get_text().split("\r")
        mots_1 = mots[1].split(" ")
        mots_2 = mots[0].split(" ")
        type.append(mots_2[1]+" "+mots_1[12]+" "+mots_1[13])

    #Chercher bethroom et bedroom
    bethroom = list()
    bedroom = list()
    property_options = html.find_all("div", attrs={"class": "property-options"})
    for prop_opt in property_options:
        mots = prop_opt.get_text().split("\n")
        if len(mots) < 2 or mots[1] == "":
            bethroom.append(np.NAN)
        else:
            bethroom.append(mots[1])
        if len(mots) < 3 or mots[2] == "":
            bedroom.append(np.NAN)
        else:
            bedroom.append(mots[2])

    #Chercher price
    price = list()
    property_price = html.find_all("div", attrs={"class": "property-price"})
    for prop_price in property_price:
        mots = prop_price.get_text().split("\n")
        mots = mots[1].split(" ")
        mots = [x for x in mots if x != ''] #Remove empty strings from a list
        price.append(mots[0].replace('\xa0', ' ')+'$')

    #Chercher adresse + Timestamp
    adress = list()
    i = 0
    property_address_street = html.find_all("span",attrs={"class": "property-address-street"}) #property-address
    property_address_locality = html.find_all("span",attrs={"class": "property-address-locality"}) #property-address
    now = datetime.now()
    for prop_street in property_address_street:
        adress.append(prop_street.get_text())
    for prop_local in property_address_locality:
        adress[i] = adress[i]+prop_local.get_text()
        i+=1

    # Ajouter les valeurs au Dataframe
    data={'Timestamp':now, 'ULS':uls, 'Type':type, 'Adresse':adress, 'Bethroom':bethroom, 'Bedroom':bedroom, 'Price':price}
    df = pd.DataFrame(data)
    # print(df)
    return df

def add_data_to_file(report):
    with open("montreal_data.txt", "a", newline="") as ficout:
        ecriteur = csv.writer(ficout, delimiter="|", quoting=csv.QUOTE_NONNUMERIC)
        for i, row in report.iterrows():
            ecriteur.writerow((row["Timestamp"], row["ULS"], row["Type"], row["Adresse"], row["Bethroom"], row["Bedroom"], row["Price"]))

if __name__ == '__main__':
    main()
