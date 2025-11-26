# https://www.pluralsight.com/guides/guide-scraping-media-from-the-web-python
# https://pypi.org/project/requests-ntlm2/
# https://github.com/requests/requests-ntlm

from lxml import html, etree
import requests
from requests_ntlm import HttpNtlmAuth
import pandas as pd
from bs4 import BeautifulSoup
import csv
import re
import os
import sys

session = requests.Session()
session.auth = HttpNtlmAuth('saugat.bhattarai', 'Password')
response = session.get('https://dystonia.wustl.edu/')
print(response)

def getVideosName(url):

    page = open(url)
    # # Parse HTML code for the entire site
    soup = BeautifulSoup(page.read(), "lxml")
    # print(soup.prettify()) # print the parsed data of html
    data = soup.find_all("table", attrs={"id": "gvResults"})

    # Lets go ahead and scrape first table with HTML code gdp[0]
    table1 = data[0]
    # the head will form our column names
    body = table1.find_all("tr")
    # Head values (Column names) are the first items of the body list
    head = body[0]  # 0th item is the header row
    body_rows = body[1:]  # All other items becomes the rest of the rows

    # Lets now iterate through the head HTML code and make list of clean headings
    # Declare empty list to keep Columns names
    headings = []
    for item in head.find_all("th"):  # loop through all th elements
        # convert the th elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(item)
    print(headings)

    # Next is now to loop though the rest of the rows
    # print(body_rows[0])
    all_rows = []  # will be a list for list for all rows
    for row_num in range(len(body_rows)):  # A row at a time
        row = []  # this will old entries for one row
        # loop through all row entries
        for row_item in body_rows[row_num].find_all("td"):
            # row_item.text removes the tags from the entries
            # the following regex is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
            # append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)

    # We can now use the data on all_rowsa and headings to make a table
    # all_rows becomes our data and headings the column names
    df = pd.DataFrame(data=all_rows, columns=headings)
    df.head()

    video_names = df['Video'].tolist()

    return video_names


def downloadFile(AFileName):
    # extract file name from AFileName
    filename = AFileName.split("/")[-1]
    print('filename ..', filename)
    # download image using GET
    rawImage = session.get(AFileName, stream=True)
    # rawImage.raise_for_status()
    print('raw image ', rawImage)
    print('Image headers', rawImage.headers['Content-Type'])
    print('Persist headers auth', rawImage.headers)

    # save the image recieved into the file
    with open(filename, 'wb') as fd:
        for chunk in rawImage.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
    return


# downloadFile(
#     "http://www.howtowebscrape.com/examples/media/images/BigRabbit.mp4")

# downloadFile("https://dystonia.wustl.edu/Project3Dys1_20110223_scope/Project3Dys1_20110223_scope.mp4")

# Main function starts hera
# URL CALL
if __name__ == "__main__":
    url = 'dystonia_voice_speech.html'
    videos_list = getVideosName(url)
    
    path = '.' #path to current directory
    files = os.listdir(path)
    for video in videos_list:
        video_mp4 = video+'.mp4'
        print('video mp4', video)
        if not video_mp4 in files:
            print(video+ 'is downloading ...')
            downloadFile(
                "https://dystonia.wustl.edu/"+video+"/"+video+".mp4")
            print(video+' downloaded!')
        else: 
            print('Already Downloaded. Looking for new.')
