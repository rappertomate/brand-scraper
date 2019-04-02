# TODO: timeit for request and then for parsing

import os

import requests
from bs4 import BeautifulSoup

# https://inforintelligence.com/
# https://gospooky.com/
# https://www.stackoverflowbusiness.com/talent/case-studies
URL = 'https://inforintelligence.com/'
KEYWORDS = ('partner', 'client', 'testimonial', 'case', 'study', 'studies')

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
data = list(soup.select('div[class*=row]'))  # may avoid list()


def parse_partner_name(img_tag):
    if 'alt' in img_tag.attrs:  # 'alt' may contain bs
        print(img_tag.attrs['alt'])
    else:
        src = img_tag.attrs['src']
        file_name = os.path.splitext(os.path.basename(src))[0]
        print(file_name)


def check_tag_keywords(tag):
    if 'class' in tag.attrs:
        class_str = ''.join(tag.attrs['class'])
    else:
        class_str = ''
    for k in KEYWORDS:
        if k in class_str:
            return True
        elif 'src' in tag.attrs and k in tag.attrs['src']:
            return True
        elif 'href' in tag.attrs and k in tag.attrs['href']:
            return True

    return False


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = list(soup.select('div[class*=row]'))  # may avoid list()

    for d in data:
        imgs = list(d.find_all('img'))
        if len(imgs) > 1:  # bc partners usually appear inside list or grid
            for i in imgs:
                # search until grandparent
                if check_tag_keywords(i):
                    parse_partner_name(i)
                elif check_tag_keywords(i.parent):
                    parse_partner_name(i)
                elif check_tag_keywords(i.parent.parent):
                    parse_partner_name(i)


parse_page(URL)
