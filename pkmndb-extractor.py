"""
Pokemon Card Database Extractor
author: rossbot
description:
A tool to gather information about Pokemon card sets from
Bulbapedia and export them into an SQL database file
"""
import sqlite3, nltk, sys, re
from urllib import urlopen
from bs4 import BeautifulSoup


#ask user for page to get data from
address = raw_input("Enter the URL from which to get the card data> ")
html = urlopen(address).read()
#html = html[html.index('<h2><span class="mw-headline" id="Card_lists">Card lists</span></h2>'):]

soup = BeautifulSoup(html)

# get title of set
title = re.match(r'^[a-zA-z0-9 ]+', soup.title.string).group(0)
title = title.strip()

print "\n\n"
print "Set: " + title
print "---------------------------------------------------------"

table = soup.find("table", attrs={"width":"100%"})

headings = [th.get_text() for th in table.find("tr").find_all("th")]
headings = [heading.strip() for heading in headings[:]]

for heading in headings:
    print heading + "\t" ,
print "\n"

datasets = []
for row in table.find_all("tr")[1:]:
    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    datasets.append(dataset)
datasets = [[(item[0],item[1].replace('\n', '').replace(u'\u2640', '(F)').replace(u'\u2642', '(M)').replace(u'\xe9', 'e').replace(u'\u2014', '')) for item in row] for row in datasets[:]]
datasets = [row for row in datasets[:] if len(row) == 5]
#print datasets

for row in datasets:
    print "{0}\t{1}\t{2}\t{3}\t{4}".format(row[0][1].strip(), row[1][1], row[2][1], row[3][1], row[4][1])

tabletitle = title.replace(' ', '_')
con = sqlite3.connect('pkmncards.db')
with con:
    cur = con.cursor()
    command = "CREATE TABLE {}(No TEXT, Name TEXT)".format(tabletitle)
    cur.execute(command)
    for row in datasets:
        command2 = "INSERT INTO {0} VALUES('{1}', '{2}')".format(tabletitle, row[0][1].strip(), row[2][1].strip().replace("'","").replace(' ', '_'))
        print command2
        cur.execute(command2)
