from bs4 import BeautifulSoup
from PIL import Image
import requests
import os
import shutil


# Taken from http://stackoverflow.com/questions/23793987/python-write-file-to-directory-doesnt-exist
# Taken from http://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if os.path.isdir(path):
            pass
        else:
            raise


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w+b')


URL = 'http://readsnk.com/'

r = requests.get(URL)
responseBody = r.text

soup = BeautifulSoup(responseBody, 'html.parser')
chapterList = soup.find('ul', {'class': 'chapters-list'}).find_all('a')

for chapter in chapterList:
    chapterLink = chapter['href']
    chapterNumber = chapterLink.partition('chapter-')[2][:-1]

    r = requests.get(chapterLink)
    chapterBody = r.text

    soup = BeautifulSoup(chapterBody, 'html.parser')
    imageList = soup.find_all('img', {'class': 'pages__img'})

    pdfList = []
    counterImage = 1
    ext = '.pdf'
    imageLocation = r'\SNK\{}'.format(chapterNumber + ext)

    for image in imageList:
        imageLink = image['src'].rstrip()
        imageNumber = '/' + str(format(counterImage, '03'))

        # print imageLocation

        try:
            r = requests.get(imageLink, stream=True)
            if r.status_code == 200:
                im = Image.open(r.raw)
                pdfList.append(im.convert('RGB'))
        except:
            pass

        counterImage += 1

    pdfList[0].save(r'C:\Users\JP\Desktop' + imageLocation ,save_all=True, append_images=pdfList)
