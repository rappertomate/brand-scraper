import sys
from urllib.parse import urlparse

import vcr
import pytest

from src.brandparse import parser

TEST_DATA = [
    (
        'https://inforintelligence.com/',
        {
            'First slide', 'AkzoNobel', 'Randstad', 'Achmea'
        }  # confused with alt label "First slide"
    ),
    (
        'https://gospooky.com/',
        {
            'rituals', 'mtv', 'chocomel', 'unicef', 'tikkie', 'mojo', 'jbl',
            'jde', 'nederlandseloterij', 'klm', 'ikea', 'hema'
        }  # works
    ),
    (
        'https://www.stackoverflowbusiness.com/talent/case-studies',
        {
            'stratton', 'Loyalty one', 'rakuten', 'noun',
            'washington post', 'just eat', 'trivago', 'doximity',
            'force therapeutics', 'here', 'Server Density'
        }  # some brands not tagged with keyword
    ),
    (
        'https://www.bamboohr.com/customers/',
        {
            'SecurityMetrics',
            'F.H. Furr Plumbing, Heating, Air Conditioning & Electrical',
            'Corient Capital Partners', 'Beans & Brews',
            'Mission Neighborhood Centers, Inc.', 'Freshbooks',
            'Peju Province Winery', 'Synergy Surgicalists', 'Remote-Learner',
            'Smith Marion & Co', 'Purple, Rock, Scissors',
            'Island Institute',
            'International Scholarship and Tuition Services, Inc. (ISTS)',
            'Grammarly', 'Gulf Coast Water Authority', 'Canndescent',
            'BDH Global Advisors', 'Impraise', 'Postmates',
            'Certified Angus Beef', 'Jones & DeMille Engineering',
            'Serious Labs', 'Stance', 'BDG architecture design', '99designs',
            'Kinetic Physical Therapy & Wellness', 'Reddit', 'USA Football',
            'Klassen Corporation', 'Integrity IT Solutions', 'Quora',
            'US Center for SafeSport', 'Sloan Lubrication Systems',
            'Kingsway Church-New Jersey', 'Solink', 'WB Moore Company',
            'ENERGY Worldnet, Inc', 'S.W. Cole Engineering', 'New Moms', 'Dsco',
            'FanDuel', 'American Cedar & Millwork', 'Matthew 25 Aids Services',
            'Foursquare', 'Unbounce', "The Children's Gym",
            'WatchGuard Technologies, Inc.', 'Forcura', 'ZipRecruiter',
            'Jacksonville Jaguars', 'Poo~Pourri', 'The Training Associates',
            'United Vein Centers', 'Vimeo', 'Asana',
            'Insurance Council of Texas (ICT)', 'Tang Capital Management, LLC.',
            'College Housing Northwest', 'SoundCloud', 'Capcom',
            'Donaldson Capital Management', 'Branch Pattern', 'Hoffman Nursery',
            'Canva', 'GU Energy', 'iTrellis', 'Spikeball',
            'University of Maryland', 'Wistia', 'Jackrabbit Technologies',
            'Left', 'DecisivEdge', 'Jane.com'
        }  # works
    ),
    (
        'https://www.heartbeatai.com/',
        {
            'Unilever', 'Epsilon', 'Beacon'
        }  # images not labeled, test will fail anyways
    ),
    (
        'https://www.filament.ai/',
        {
            'HSBC', 'Sita', 'American Express'
        }  # divs not labeled, test will fail anyways
    )
]


@pytest.mark.parametrize('url,expected', TEST_DATA)
def test_parser(url, expected):
    domain_parts = urlparse(url).hostname.split(".")
    page_name = (
        domain_parts[0]
        if domain_parts[0] != 'www'
        else domain_parts[1])

    with vcr.use_cassette('test/fixtures/vcr_{}.yml'.format(page_name)):
        assert parser.parse_page(url) == expected
