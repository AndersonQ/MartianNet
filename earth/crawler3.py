# coding: UTF-8

## IMPORTS  ##
import string
from sys import argv
from urllib.request import urlopen # opens urls
from bs4 import BeautifulSoup # parses html

## FUNCTIONS ##
# file writing function
def writeFile(filename, data):
	f = open(filename, 'w')
	f.write(data)
	f.close

## INPUTS ##
target = 'http://en.wikipedia.org/wiki/Glasgow' # target url
nlinks = 10 # number of links to pre-load

## LOOP ##
# opens the url
mypage = urlopen(target)

soup = BeautifulSoup(mypage)
title = str(soup.title)
slicedtitle = title[7:len(title)-43]

# formats html and turns it into a string
prettysoup = (soup.prettify())

#removing non ascii characters
asciisoup = [x for x in prettysoup if x in string.printable]
originalemptystring = ""
for char in asciisoup:
	originalemptystring += char

# writes the target page to file
writeFile(slicedtitle, originalemptystring)

urls = [] # list to store urls from target url page

for link in soup.find_all("a", {"class": "mw-redirect"}):
	urls.append(link.get('href'))

for url in range(0,nlinks):
	newpage = 'http://en.wikipedia.org' + urls[url]
	openpage = urlopen(newpage)
	newsoup = BeautifulSoup(openpage)
	title = str(newsoup.title)
	slicedtitle = title[7:len(title)-43]
	lamesoup = (newsoup.prettify())
	emptystring = ""
	newascii = [x for x in lamesoup if x in string.printable]
	for char in newascii:
		emptystring += char
	writeFile(slicedtitle, emptystring)