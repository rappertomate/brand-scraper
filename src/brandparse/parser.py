# TODO: timeit for request and then for parsing
# TODO: return as tuple, enrich with kind of partnership if available (client, supplier, challenge...)
# TODO: toss image if too large e.g one side > 400 -> BETTER NOT DO THIS

import os

import requests
from bs4 import BeautifulSoup

KEYWORDS = (
    'partner', 'client', 'testimonial',
    'customer', 'case', 'study', 'studies')

BLOCKWORDS = ('placeholder', 'dummy')  # black list


def parse_partner_name(img_tag):
    text = None
    src = img_tag.attrs['src']
    file_name = os.path.splitext(os.path.basename(src))[0]
    file_ext = os.path.splitext(os.path.basename(src))[1]
    file_dir = os.path.dirname(src)

    if 'alt' in img_tag.attrs:  # 'alt' may contain bs
        if img_tag.attrs['alt'].strip():
            text = img_tag.attrs['alt']

    if not text:
        text = file_name

    # clean up:

    if file_ext == '.svg':
        for w in KEYWORDS:  # keyword in path is good sign
            if w in file_dir:
                break
        else:
            return None

    for w in KEYWORDS + BLOCKWORDS:  # keyword in file name/alt text is bad sign
        if w in text:
            return None

    return text


def check_tag_keywords(tag):
    if 'class' in tag.attrs:
        class_str = ''.join(tag.attrs['class'])
    else:
        class_str = ''
    for w in KEYWORDS:
        if w in class_str:
            return True
        elif 'src' in tag.attrs and w in tag.attrs['src']:
            return True
        elif 'href' in tag.attrs and w in tag.attrs['href']:
            return True

    return False


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #data = list(soup.select('div[class*=row]'))  # may avoid list()
    data = list(soup.select('div'))  # may avoid list()
    results = set()

    for d in data:
        imgs = list(d.find_all('img'))
        if len(imgs) > 1:  # bc partners usually appear inside list or grid
            for i in imgs:
                # search until grandparent
                if check_tag_keywords(i):
                    results.add(parse_partner_name(i))
                elif check_tag_keywords(i.parent):
                    results.add(parse_partner_name(i))
                elif check_tag_keywords(i.parent.parent):
                    results.add(parse_partner_name(i))

    results.discard(None)

    return results


if __name__ == '__main__':
    results = parse_page(  # pass URL for tests here
        'https://www.stackoverflowbusiness.com/talent/case-studies')
    print(results)
