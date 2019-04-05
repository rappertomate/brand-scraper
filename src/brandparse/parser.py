# TODO: memorize route of each src. if one image has another address or much longer/short name, it is most likely sth else
# TODO: timeit for request and then for parsing
# TODO: return as tuple, enrich with kind of partnership if available (client, supplier, challenge...)
# TODO: toss image if too large e.g one side > 400 -> BETTER NOT DO THIS

import os

import requests
from bs4 import BeautifulSoup

KEYWORDS = (
    'partner', 'client', 'testimonial',
    'customer', 'case', 'study', 'studies')


def parse_partner_name(img_tag):
    if 'alt' in img_tag.attrs:  # 'alt' may contain bs
        return img_tag.attrs['alt']
    else:
        src = img_tag.attrs['src']
        file_name = os.path.splitext(os.path.basename(src))[0]
        return file_name


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

    return results


def clean_results(result_set):
    result_set.remove("")

    non_set = set()
    for r in result_set:
        if not r.strip():  # maybe strip everything initially
            non_set.add(r)
            continue
        for k in KEYWORDS:
            if k in r:
                non_set.add(r)

    return result_set - non_set


if __name__ == '__main__':
    results = parse_page(
        'https://www.stackoverflowbusiness.com/talent/case-studies')
    cleaned = clean_results(results)
    print(cleaned)
