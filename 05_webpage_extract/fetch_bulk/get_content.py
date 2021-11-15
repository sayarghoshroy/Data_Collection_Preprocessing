import json
import time
import tqdm
from boilerpipe.extract import Extractor

def get_content(url):
    
    if display:
        print("Trying URL ~ " + str(url), flush = True)
    
    try:
        extractor = Extractor(extractor = 'ArticleExtractor', url = url)
        # Try out extractor.getHTML()
        text = str(extractor.getHTML())
        mapping = [url, text]

        if display:
            print("URL ~ " + str(url) + " : Successful Retrieval", flush = True)
        
        return mapping

    except Exception as E:
        
        if display:
            print('Exception: ' +str(E))
            print("URL ~ " + str(url) + " : Retrieval Failed", flush = True)

        mapping = [url, "!FAILURE!"]
        return mapping

if __name__ == '__main__':

    display = True

    with open('./urls.json', 'r+') as file:
        collection = json.load(file)

    collection_size = len(collection)
    # collection stores the list of URLs

    print("Number of URLs: " + str(collection_size), flush = True)

    begin = time.time()

    results = {}

    for item in collection:
        output = get_content(item)
        key = output[0]
        extracted = output[1]

        results[key] = extracted

    end = time.time()
    duration = int(end - begin)
    print()
    print("Time Taken: " + str(int(duration / 60)) + " minutes, " + str(int(duration % 60)) + " seconds", flush = True)

    print()
    count_proper = 0
    for item in results:
        if item[1] != '!FAILURE!':
            count_proper += 1

    print('Number of Successful Retrievals: ' + str(count_proper))

    # Dump Contents onto JSON
    with open('./content_set.json', 'w+') as file:
        json.dump(results, file)

# Done