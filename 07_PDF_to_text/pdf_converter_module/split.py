import os
import re

with open("./PDFs_texts/2.txt", "r+") as fp:
    text = fp.read()

def page_split_proto():
    # Specific to types of PDFs
    # Advanced: Figure out what the headings are

    global text
    
    expression_a = "© STL Partners \nEXECUTIVE BRIEFING \nTHE IOT IS DEAD: LONG LIVE THE I4T – THE INTERNET FOR THINGS | MAY 2019"

    pages = (re.split(expression_a, text))

    pages = list(filter(lambda x : x != "|", pages))

    wf = open("final.txt", "w+")

    for page in pages:
        wf.write(page)
        wf.write("\n[END_OF_PAGE]\n")

    print("Number of Pages : ", (len(pages)))

page_split_proto()