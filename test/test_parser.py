import sys
from urllib.parse import urlparse

import vcr
import pytest

from src.brandparse import parser

TEST_DATA = [
    (
        'https://inforintelligence.com/',
        {
            'first slide', 'akzonobel', 'achmea', 'randstad'
        }
    ),
    (
        'https://gospooky.com/',
        {
            'rituals', 'mtv', 'chocomel', 'unicef', 'tikkie', 'mojo', 'jbl',
            'jde', 'nederlandseloterij', 'klm', 'ikea', 'hema'
        }
    ),
    ('https://www.stackoverflowbusiness.com/talent/case-studies', True),
    ('https://www.bamboohr.com/customers/', True)
]


@pytest.mark.parametrize('url,expected', TEST_DATA)
def test_parser(url, expected):
    domain_parts = urlparse(url).hostname.split(".")
    page_name = (
        domain_parts[0]
        if domain_parts[0] != 'www'
        else domain_parts[1])

    with vcr.use_cassette('test/fixtures/vcr_{}.yml'.format(page_name)):
        parser.parse_page(url)
        assert True == expected
